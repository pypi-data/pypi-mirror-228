'''对pandas的frame进行方法扩展
经历了多种实现过程
1. pytraits3存在版本兼容性问题，仅在较低版本python上可以正常跑起来
2. 使用types包，但是由于修改了DataFrame的__getitem__和__getattr__方法，使得[]和.操作得到的依旧可以使用扩展的方法
3. 继承，目前使用该方法在做
'''
import traceback
import pandas
from ..models import GeMatrix, GeMatrixPie
from .schema import schemacenter
from ..preprocessing.feature_transform import TypeTransform, NanTransform, SparseTransform, CustomTranform
from ..preprocessing.feature_transform import VarlenSparseTransform, DenseTransform, DefaultTransform
from ..preprocessing import DataSplit
from ..preprocessing.feature_selection import NanFeatureSelect, CorrlationFeatureSelect, EntropyFeatureSelect
from ..preprocessing.feature_selection import VarianceFeatureSelect, IvFeatureSelect, MonotonicityFeatureSelect
from inspect import isfunction
from ..visualization import LineChartPercent, LineChartPercentKde, LineChartPercentHue, LineChartPercent2Group
from ..visualization import HeatMapPercent, FeatureDistribution, SankeyOne, Sankey
from .series import Series


class DataFrame(pandas.DataFrame):
    '''从DataFrame继承，可以使用pandas的各类方法
    '''
    def __getitem__(self, key):
        # df[key] 操作可以增加pa_方法
        res = super().__getitem__(key)
        if isinstance(res, pandas.core.frame.DataFrame):
            return DataFrame(res)
        elif isinstance(res, pandas.core.series.Series):
            return Series(res)
        else:
            return res

    def __getattr__(self, name: str):
        # df.name 操作可以增加pa_方法
        return Series(super().__getattr__(name))

    def pa_schema(self, feat_names=None):
        '''描述字段解释
        '''
        # res = []
        # # 未指定feat_name，则返回全部特征解释，默认情况
        # if feat_names is None:
        #     feat_names = self.columns
        # # 指定多个特征
        # elif isinstance(feat_names, (tuple, list)):
        #     pass
        # # 指定单个特征
        # elif isinstance(feat_names, str):
        #     feat_names = [feat_names]

        # for feat_name in feat_names:
        #     if schemacenter[feat_name]:
        #         res.append(schemacenter[feat_name].property)
        #     else:
        #         print(f'[Warning] {feat_name} not in schemacenter')
        # return pandas.DataFrame(res)

        if feat_names is None:
            feat_names = self.columns
        return schemacenter.pa_schema(feat_names)

    def pa_add_schema(self, params, replace=False):
        '''增加字段的说明等等，尤其是sql语句中新拉出来的特征
        
        :param params: 多个特征描述用[]来组织
        '''
        schemacenter.pa_add_schema(params, replace)


    def pa_describe(self, importance_dict={}, schema_columns=()):
        '''用于展示选出来特征的分布，如特征重要性，含iv，特征缺失率，信息熵等
        
        :param importance_dict: dict, {fea: v}的字典类型
        :param schema_columns: tuple/list, 额外展示的列名
        '''
        res = []
        for col in self.columns:
            res_one = {
                    'name': col, 
                    'definition': None, 
                    'importance': importance_dict.get(col), 
                    'dtype': self[col].dtype, 
                    'count': self[col].count(), 
                    'notna_ratio': self[col].count()/self[col].size, 
                    'nunique': self[col].nunique(),
                    'rand_example': self.loc[~self[col].isna(), col].sample(n=1).iloc[0] if sum(~self[col].isna())>0 else None,
                    }

            col_schema = self[col].pa_schema()
            res_one['definition'] = res_one['name'] if col_schema is None else col_schema['definition']
            res_one.update({i:None if col_schema is None else col_schema[i] for i in schema_columns})
            res.append(res_one)
        res = pandas.DataFrame(res)

        # drop掉无意义的列
        drop_cols = []
        for col in res.columns:
            if (~res[col].isna()).sum() == 0:
                drop_cols.append(col)
        res.drop(drop_cols, axis=1, inplace=True)
        return res

    def pa_feature_transform(self, method='default', dense_list=[], sparse_list=[], register=None, inplace=False, 
                             sparse_nan_fill='raw', dense_nan_fill='raw', sparse_encode='raw', dense_encode='raw', **params):
        '''对特征进行转换处理

        :param method: 处理方式，默认为default方式，当特征维护了默认处理方式时候可以适用
        :param register: 是否注册，用于记录数据处理中的编码规则，如需注册，则应传入具体的值
        :param inplace：是否inplace操作，设置为True则表示本地修改，默认为False
        :param dense_list: 连续变量列表
        :param sparse_list: 离散变量列表
        :param sparse_nan_fill: 离散变量nan填充方式，可选'raw'表示不填充，也可以给定固定值如0填充
        :param dense_nan_fill: 连续变量nan填充方式，可选'raw'表示不填充，'average'表示均值填充，也可以给定固定值如-1填充
        :param sparse_encode: 离散变量编码方式
            raw: 不作处理
            dummy: onehot编码
            label_encoder：直接映射到0,1,2,...
            dict_encoder：自己实现的label_encoder, 不依赖sklearn，且有default值
            dict: 和label_encoder类似，但是有顺序之分
            woe: woe编码
        :param dense_encode: 连续变量编码方式
            raw: 不作处理
            std_scale: StandardScaler
            min_max_scale: MinMaxScaler()
        '''
        if isinstance(method, str) or isfunction(method):
            method = [method]

        params_cp = params.copy()
        params_cp['inplace'] = inplace
        params_cp['dense_list'] = dense_list
        params_cp['sparse_list'] = sparse_list
        params_cp['sparse_nan_fill'] = sparse_nan_fill
        params_cp['dense_nan_fill'] = dense_nan_fill
        params_cp['sparse_encode'] = sparse_encode
        params_cp['dense_encode'] = dense_encode

        for item in method:
            if item == 'default':
                trans = DefaultTransform(**params_cp)
            elif item == 'nan':
                trans = NanTransform(**params_cp)
            elif item == 'sparse':
                trans = SparseTransform(**params_cp)
            elif item == 'dense':
                trans = DenseTransform(**params_cp)
            elif item == 'varlen_sparse':
                trans = VarlenSparseTransform(**params_cp)
            elif isfunction(item):
                trans = CustomTranform(item, **params_cp)
            else:
                raise ValueError(f'Args `method` {item} is not allowed')
            
            if inplace:
                trans.fit(self)
            else:
                df = trans.fit(self)[0]  # 只返回X
            if register is not None:
                # 记录训练特征处理流程
                register.append(trans)
            if not inplace:
                return DataFrame(df)
    
    def pa_default_dtypes(self, skip_fea_list=[], **params):
        '''根据字段类型区分sparse, dense变量

        :param skip_fea_list: 需要跳过的特征
        '''
        trans = TypeTransform(skip_fea_list, **params)
        trans.fit(self)
        res = {'sparse_list': trans.sparse_list, 
               'dense_list': trans.dense_list,
               'varlen_sparse_list': trans.varlen_sparse_list}
        return res

    def pa_convert_dtypes(self, inplace=False):
        '''依据feature.xlsx中维护的字段类型，对df进行类型转换
        '''
        if not inplace:
            df_new = self.copy()

        for col in self.columns:
            try:
                if inplace:
                    self[col] = self[col].pa_convert_dtypes()
                else:
                    df_new[col] = df_new[col].pa_convert_dtypes()
            except:
                print(traceback.format_exc())
        
        return None if inplace else df_new

    def pa_plot(self, method='hist_distribution', tgt_name=None, sparse_list=[], dense_list=[], 
                save_path=None, bin_count=10, figsize=(20,20), **params):
        '''输出各类特征的分布图

        :param method: 
            特征分布：kde_distribution, hist_distribution, count_distribution, joyplot_distribution, kde_distribution_2d, hist_distribution_2d
            二/多分类用户占比折线图：line_chart_percent
            二分类用户占比热力图：heat_map_percent
        :param tgt_name: 目标特征名，仅在method设置为line_chart_percent和heat_map_percent时需要
        :param dense_list: 连续变量列表
        :param sparse_list: 离散变量列表
        :param save_path: 图保存的目录，默认不保存
        :param bin_count: qcut的分箱数量
        :param figsize: 图片的大小
        '''
        params_cp = params.copy()
        params_cp['sparse_list'] = sparse_list
        params_cp['dense_list'] = dense_list
        params_cp['save_path'] = save_path
        params_cp['bin_count'] = bin_count
        params_cp['figsize'] = figsize

        if method in {'kde_distribution', 'hist_distribution', 'count_distribution', 'joyplot_distribution', 'kde_distribution_2d', 'hist_distribution_2d'}:
            # 特征分布
            plot_ = FeatureDistribution(method=method, **params_cp)
        elif method == 'line_chart_percent':
            # 二/多分类用户占比折线图
            plot_ = LineChartPercent(**params_cp)
        elif method == 'line_chart_percent_2group':
            # 二分类用户占比折线图，在LineChartPercent修改，柱状图修改为stack柱状图，折线图修改为两类用户占比
            plot_ = LineChartPercent2Group(**params_cp)
        elif method == 'line_chart_percent_hue':
            # 二分类用户占比折线图, 按照hue拆分，就是把多个LineChartPercent放在一张图上
            plot_ = LineChartPercentHue(**params_cp)
        elif method == 'line_chart_percent_kde':
            # 二/多分类用户占比kde图，即把LineChartPercent的柱状图改为kde图，折线部分还需要再debug下
            plot_ = LineChartPercentKde(**params_cp)
        elif method == 'heat_map_percent':
            # 二分类用户占比热力图
            plot_ = HeatMapPercent(**params_cp)
        else:
            raise ValueError(f'Args `method` {method} is not allowed')

        x_cols = [col for col in self.columns if col != tgt_name]
        plot_.fit(self[x_cols], self[tgt_name] if tgt_name else None)

    def pa_ge_matrix(self, index, columns, method='gematrix', save_path='', figsize=(8,8), index_bins=None, columns_bins=None, 
                     dense_bin_count=10, dense_cut_mode='cut', sparse_fea_sort={}, **params):
        '''客户在宫格GE矩阵上的分布表和分布图

        :param index: 行名
        :param columns: 列名
        :param method: 绘图方式，可选'gematrix'和'gematrix_pie'
        :param save_path: 图保存的目录
        :param index_bins: 需要手动指定index的切分边界，默认为None
        :param columns_bins: 需要手动指定index的切分边界，默认为None
        :param sparse_fea_sort: {fea: [fea_list]}, 仅对离散变量配置，用于指定离散变量的排列顺序
        :param dense_bin_count: 连续值需要划分的箱体数量，若指定了index_bins/column_bins，则不生效
        :param dense_cut_mode: 连续变量是使用cut还是qcut
        :param cal_density: 是否计算格子的密度，即绘制出来是比例
        :param figsize: 绘制的figure尺寸
        :param choice: default, add_margin_subplots(subplots方式添加边缘分布), add_margin_gridsepc(gridsepc方式添加边缘分布)
        '''
        params_cp = params.copy()
        params_cp['save_path'] = save_path
        params_cp['figsize'] = figsize
        params_cp['index_bins'] = index_bins
        params_cp['columns_bins'] = columns_bins
        params_cp['dense_bin_count'] = dense_bin_count
        params_cp['dense_cut_mode'] = dense_cut_mode
        params_cp['sparse_fea_sort'] = sparse_fea_sort

        if method == 'gematrix':
            ge_ = GeMatrix(index, columns, **params_cp)
        elif method == 'gematrix_pie':
            ge_ = GeMatrixPie(index, columns, **params_cp)
        return ge_.fit(self, None)

    def pa_data_split(self, tgt_name, method='train_test_split', split_options={'test_size': 0.2}, return_dataframe=False, **params):
        '''数据切分

        :param tgt_name: 目标特征名
        :param method: 可选'train_test_split', 'StratifiedKFold', 'StratifiedShuffleSplit'
        :param split_options: 切分用到的参数
        :param return_dataframe: 是否返回切分后的dataframe，若为True则只返回切分的index
        '''
        params_cp = params.copy()
        params_cp['tgt_name'] = tgt_name
        params_cp['method'] = method
        params_cp['split_options'] = split_options
        params_cp['return_dataframe'] = return_dataframe

        split_ = DataSplit(**params_cp)

        x_cols = [col for col in self.columns if col != tgt_name]
        return split_.fit(self[x_cols], self[tgt_name])

    def pa_feature_select(self, method='nan', topk=1000, tgt_name=None, sparse_list=[], dense_list=[], **params):
        '''特征选择

        :param method: 可选'nan', 'iv', 'corrlation', 'entropy', 'variance', 'increase_decrease'
        :param topk: 返回数量
        :param tgt_name: iv使用
        :param sparse_list： iv使用
        :param dense_list: iv使用
        '''
        params_cp = params.copy()
        params_cp['topk'] = topk
        params_cp['dense_list'] = dense_list
        params_cp['sparse_list'] = sparse_list

        x_cols = [col for col in self.columns if col != tgt_name]

        if method == 'nan':
            # 缺失率
            select_ = NanFeatureSelect(**params_cp)
        elif method == 'iv':
            # iv
            if tgt_name not in self.columns:
                raise ValueError(f'{tgt_name} not in dataframe columns')
            select_ = IvFeatureSelect(**params_cp)
        elif method == 'corrlation':
            # 按照特征相关性
            select_ = CorrlationFeatureSelect(**params_cp)
        elif method == 'entropy':
            # 按照特征的信息熵
            select_ = EntropyFeatureSelect(**params_cp)
        elif method == 'variance':
            # 按照特征的方差
            select_ = VarianceFeatureSelect(**params_cp)
        elif method in {'increase_decrease', 'monotonicity'}:
            # 按照单调性
            select_ = MonotonicityFeatureSelect(**params_cp)
        else:
            raise ValueError(f'`Method`={method} not in ("nan", "iv", "corrlation")')
        return select_.fit(self[x_cols], self[tgt_name] if tgt_name else None)
        
    def pa_compare_users(self):
        '''不同特征上客户的分布表和分布图，特征的差异性指标
        '''
        pass

    def pa_sankey(self, labels, method='one', **params):
        '''桑基图
        
        :param labels: 绘制使用的字段名，或者字段+条件
        :param method: 可选'one'和'multi', 'one'表示按照条件删选的绘制，'multi'为一般桑基图
        '''
        if method == 'one':
            sankey = SankeyOne(labels, **params)
        elif method == 'multi':
            sankey = Sankey(labels, **params)
        sankey.fit(self)


if __name__ == '__main__':
    import numpy as np
    df = pandas.DataFrame(np.random.rand(5, 10))
    df.transform()
    df.columns = [f'fea_{i}' for i in range(df.shape[1])]
    df['target'] = np.random.randint(0, 2, 5)
    print(df)
    assert hasattr(df, 'transform')
    assert hasattr(df, 'explain')
    assert hasattr(df, 'plot')
    assert hasattr(df, 'plot2d')
    assert hasattr(df, 'ge_matrix')
    assert hasattr(df, 'feature_select')
