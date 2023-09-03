from abc import abstractmethod, ABCMeta
import pandas as pd
import warnings
from ..data import Feature, schemacenter, DataFrame
import traceback
import os

# class DadaLoader(metaclass=ABCMeta):
#     '''通过接口Interface来实现
#     '''
#     @abstractmethod
#     def load(self):
#         # 数据加载
#         pass


def merge_features(*features, verbose=0):
    '''features的合并
    '''
    features_new = dict()
    for feature in features:
        for name, feat in feature.items():
            if (name in features_new) and (verbose != 0):
                print(f'Got multiple values for keyword argument `{name}`')
            features_new[name] = feat
    return features_new

def adjust_columns(columns, prefix):
    '''去除DataFrame的columns的前缀
    '''
    if prefix is None:
        return columns

    if isinstance(prefix, str):
        prefix = [prefix]

    columns_new = []
    for col in columns:
        for item in prefix:
            col = col.replace(item, '')
        columns_new.append(col)
    return columns_new
    

def datatools_fetch(um, SQL, column_prefix=None, duplicated=True, verbose=0, save_path=None):
    '''用datatools执行对应的sql, 获取数据

    um: 员工um号
    SQL: 待执行的SQL
    column_prefix: 去除列名前缀，一般是['a.', 'b.’]等
    duplicated: 去除重复列
    verbose: 打印SQL
    '''
    if verbose!=0:
        print(SQL)
    
    if save_path is not None:
        # 创建文件夹
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # 从本地文件恢复
        if os.path.exists(save_path):
            print(f'[INFO] resume data from local cached file: {save_path}')
            return DataFrame(pd.read_pickle(save_path))

    from datatools.data_tools import DataTools
    datatools_source = DataTools(um=um)
    hive_client_source = datatools_source.get_hive_client()
    data = DataFrame()
    try:
        data = hive_client_source.fetch_data_to_df(SQL)
        data = DataFrame(data)
    except:
        print(f"hive sql query error for query {SQL}")
        print(traceback.format_exc())
    
    # 去除列名前缀
    if column_prefix:
        data.columns = adjust_columns(data.columns, column_prefix)
    # 去除重复列
    if duplicated:
        data = data.loc[:, ~data.columns.duplicated()]
    data = DataFrame(data)

    # 保存文件到本地
    if save_path is not None:
        if len(data) > 0:
            data.to_pickle(save_path)
            print(f'[INFO] save data to local cached file: {save_path}')

    return data


def datatools_save(um, df, table_name, dt):
    '''用datatools执行对应的sql, 保存数据到hive

    um: 员工um号
    df: 需要保存的dataframe
    table_name: 表名，如wia_robot.table_test
    dt: 保存的dt分区，如20230101
    '''
    from datatools.data_tools import DataTools
    datatools_source = DataTools(um=um)
    hive_client_source = datatools_source.get_hive_client()
    try:
        hive_client_source.save_df_to_table(df, table_name, 'dt={}'.format(dt))
    except:
        print("hive sql save error for table {}").format(table_name)
    return


class DataLoader(object):
    '''基类
    '''
    def __init__(self, source_um, pri_key, sheet_name) -> None:
        super().__init__()
        # 初始化该dataloader的特征
        self.table_name, feature_list = schemacenter.initialize(sheet_name=sheet_name)
        # 从schema提取
        self.features = schemacenter.get_items(feature_list)
        self.source_um = source_um
        self.pri_key = pri_key  # 主键
        self.query_hive = True  # 定义是否执行取数，debug时候使用

    def load(self, dt, target_sql=None, join_on=None, join_on_dt=False, pri_key_list=None, feature_list=None, how='inner', 
             convert_dtypes=True, verbose=0, save_path=None, **params):
        ''' base的load，由于下层load的写法基本一致，这里提取到基类中实现

        :param dt: 必须字段，获取数据的日期，examples: 20221114, '20221114', [20221113, 20221114]
        :param target_sql: 非必须字段，取用y的sql, 至少包含用于join的字段
        :param join_on: 非必须字段，target_sql不为None时候使用，是target_sql中用于join的字段名
        :param join_on_dt: 是否使用dt来join
        :param pri_key_list: 非必须字段，主键列表（可以是用户列表，基金列表等），只取部分样本时候使用
        :param feature_list: 非必须字段，特征列表，可以是str/list类型，只取其中的部分特征时候使用
                             - None/'recommend'表示仅加载推荐字段
                             - 'all'表示加载全部字段
                             - tuple/list表示按指定特征列表加载
        :param how: join方式，默认为inner join
        :param convert_dtypes: 修改字段类型
        :param save_path: str，取到的数据存放的位置
        '''
        SQL = self.gen_sql(dt, target_sql, pri_key_list, feature_list)
        
        if target_sql:
            # target_sql存在
            assert how in {'left', 'inner', 'outer', 'right'}, f'Args `how`={how} illegal'
            assert join_on is not None, f'Args `join_on`={join_on} can not be None'
            assert join_on in target_sql, f'Args `join_on`={join_on} not in `target_sql`={target_sql}'

            SQL = f'''
            with table_target as({target_sql}),
            table_features as({SQL})
            select table_target.*, table_features.*
            from table_target
            {how} join table_features on table_target.{join_on}=table_features.{self.pri_key}
            '''
            if join_on_dt:
                SQL += ' and table_target.dt = table_features.dt'
        
        # 用于debug使用，不执行SQL
        if not self.query_hive:
            return SQL

        # datatools执行sql取数
        data = datatools_fetch(self.source_um, SQL, ['table_target.', 'table_features.'], verbose=verbose, save_path=save_path)
        
        # 根据feature.xlsx中维护的dtype来执行类型修改
        if convert_dtypes:
            data = data.pa_convert_dtypes()
        return self.post_process(data)

    def post_process(self, data):
        '''后处理
        '''
        return data
        
    @staticmethod
    def get_dt_str(dt):
        '''解析时间
        '''
        if isinstance(dt, (str, int)):
            dt_str = f'dt={dt}'
        elif isinstance(dt, (tuple, list)) and len(dt)==2:
            dt_str = f'dt between {dt[0]} and {dt[1]}'
        elif isinstance(dt, (tuple, list)) and len(dt)>2:
            dt_str = f"dt in ({','.join(dt)})"
        else:
            raise ValueError('`Args` dt format illegal')
        return dt_str
    
    def filter_featurs(self, feature_list):
        '''对特征进行过滤，并原地修改self.features
        '''
        # 对于未维护的特征，给予提示
        not_in_feas = []
        if (feature_list is None) or (feature_list=='recommend'):
            # 仅加载推荐特征
            self.features = {fea: feature for fea, feature in self.features.items() if feature.recommend!=0}
        elif isinstance(feature_list, (tuple, list)):
            # 加载指定特征
            not_in_feas = [fea for fea in feature_list if fea not in self.features]
            if len(not_in_feas) > 0:
                warnings.warn(f'{not_in_feas} is not maintained, please check your feature_list input')
            # 主键需要包含在feature_list
            if self.pri_key not in feature_list:
                feature_list.append(self.pri_key)
            self.features = {fea: self.features[fea] for fea in feature_list if fea in self.features}
        elif feature_list == 'all':
            # 加载全部特征
            pass
        else:
            warnings.warn(f'Args `feature_list`={feature_list} is not a valid arg, use all maintained feature instead')

    def gen_sql(self, dt, target_sql, pri_key_list, feature_list):
        '''获取SQL
        pri_key_list：样本的id的list，一般指user维度如userid的list， cust_code的list
        '''
        if target_sql is None and pri_key_list is None:
            warnings.warn('No target_sql and pri_key_list provided, may consume long time to fetch data')
        self.filter_featurs(feature_list)
        dt_str = self.get_dt_str(dt)

        # 取特征的sql
        sel_feats = [fea.sql for fea in self.features.values()]
        # fea_str.extend(not_in_feas)  # 对于未维护的特征，允许用户使用（只要底层存在该特征即可），暂时不使用，会导致sql出错
        if 'dt' not in sel_feats:
            sel_feats.append('dt')
        SQL = f"select {','.join(sel_feats)} from {self.table_name} where {dt_str}"
        
        if pri_key_list:
            SQL += f"and {self.pri_key} in ({', '.join(pri_key_list)})"
        
        return SQL

    def pa_schema(self):
        '''DataLoader描述字段解释
        '''
        res = []
        for feat_name in self.features.keys():
            if schemacenter[feat_name]:
                res.append(schemacenter[feat_name].property)
        return pd.DataFrame(res)

    def pa_add_schema(self, params, replace=False):
        '''DataLoader增加字段的说明等等，尤其是sql语句中新拉出来的特征
        params: 多个特征描述用[]来组织
        '''
        schemacenter.pa_add_schema(params, replace)
        if not isinstance(params, (tuple, list)):
            params = [params]
        self.features.update({item['name']: schemacenter[item['name']] for item in params})
