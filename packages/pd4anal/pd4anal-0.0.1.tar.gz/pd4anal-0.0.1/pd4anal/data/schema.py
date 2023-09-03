import pandas as pd
import numpy as np
import os
import warnings
import json

class Feature(object):
    def __init__(self, name, table_name=None, sql=None, definition=None, description=None, category=None, channel=None, 
                 dtype=None, enum=None, transform=None, recommend=None, **kwargs):
        self.name = name
        self.table_name = table_name
        self.sql = sql or name
        self.definition = definition or name
        self.description = description
        self.category = category
        self.channel = channel
        self.dtype = dtype
        self.enum = enum
        self.transform = transform
        self.recommend = recommend
    
    def __repr__(self):
        return json.dumps(self.property, ensure_ascii=False, indent=2)

    @property
    def property(self):
        return {'name': self.name,
                'sql': self.sql,
                'definition': self.definition,
                'description': self.description,
                'table_name': self.table_name,
                'category': self.category,
                'channel': self.channel,
                'dtype': self.dtype,
                'enum': self.enum,
                'transform': self.transform,
                'recommend': self.recommend}

class Schema(object):
    def __init__(self):
        self.schema_center = dict()  # key是特征名，value是Feature
    
    def __repr__(self):
        '''schemacenter打印有意义的信息, 这里必须是字符串'''
        repr_ = super().__repr__()
        repr_  += '\n[INFO] use `schemacenter.pa_schema()` to check all supported features.'
        repr_  += '\n[INFO] use `schemacenter[fea]` or `schemacenter.fea` to check selected feature.'

    def __call__(self, feat_names=None):
        return self.pa_schema(feat_names)

    def __getitem__(self, feat_name):
        '''schemacenter['userid']操作'''
        return self.schema_center.get(feat_name, None)

    def __getattr__(self, feat_name: str):
        '''schemacenter.userid操作'''
        return self.schema_center.get(feat_name, None)
    
    def __setitem__(self, feat_name, feat):
        '''schemacenter['userid']的赋值操作'''
        self.schema_center[feat_name] = feat
    
    def __delitem__(self, feat_name):
        '''schemacenter['userid']的删除操作'''
        del self.schema_center[feat_name]
    
    def get_items(self, feat_names):
        return {k:v for k, v in self.schema_center.items() if k in feat_names}

    def reset(self):
        self.schema_center = dict()

    def initialize(self, sheet_name=None):
        '''初始化：则返回表名, 特证列表
        '''
        dfs = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + '/features.xlsx', sheet_name=sheet_name)
        if sheet_name:
            schemacenter.pa_add_schema(dfs.to_dict('records'), replace=True)
            table_name, feature_list = dfs['table_name'][0], dfs['name'].tolist()
            return table_name, feature_list
        else:
            table_name, feature_list = [], []
            for sheet_name, df in dfs.items():
                # schemacenter由于是flat的，因此这里是replace的，即要求feature.xlsx中特征是不重名的
                schemacenter.pa_add_schema(df.to_dict('records'), replace=True)
                table_name.append(df['table_name'][0])
                feature_list.extend(df['name'].tolist())
            return table_name, feature_list

    def pa_schema(self, feat_names=None):
        '''描述字段解释
        '''
        res = []
        # 未指定feat_name，则返回全部特征解释，默认情况
        if feat_names is None:
            feat_names = list(self.schema_center.keys())
        # 指定多个特征
        elif isinstance(feat_names, (tuple, list)):
            pass
        # 指定单个特征
        elif isinstance(feat_names, str):
            feat_names = [feat_names]

        for feat_name in feat_names:
            feature = self.schema_center.get(feat_name, None)
            if feature is None:
                print(f'[Warning] {feat_name} not in schemacenter')
                continue
            # 如果key是重复项，则value是一个list，目前还是独占的
            if isinstance(feature, (tuple, list)):
                for item in feature:
                    res.append(item.property)
            else:
                res.append(feature.property)
        if len(res) > 1:
            return pd.DataFrame(res)
        else:
            return pd.Series(res[0])

    def pa_add_schema(self, params, replace=False):
        '''增加字段的说明等等，尤其是sql语句中新拉出来的特征
        params: 多个特征描述用[]来组织
        '''
        def cal_v(v):
            '''对value清洗，主要是nan替换为None
            '''
            if isinstance(v, str) and v.startswith('{') and v.endswith('}'):
                # 字符串转字典
                return eval(v)
            elif isinstance(v, (str, dict)):  # 字符串和字典直接返回
                return v
            elif np.isnan(v):
                # nan替换为None
                return None
            return v

        if not isinstance(params, (tuple, list)):
            params = [params]

        for item in params:
            if (not replace) and (item['name'] in self.schema_center):
                raise ValueError(f'{item} is already in schema_center')
            item = {k.strip(): cal_v(v) for k, v in item.items()}
            self.schema_center[item['name']] = Feature(**item)
        return self.pa_schema()

schemacenter = Schema()
schemacenter.initialize()

