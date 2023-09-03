import pandas as pd
from .schema import schemacenter
from pd4anal.utils import is_dtype_float
import numpy as np
import datetime
from inspect import isfunction


class Series(pd.Series):
    def pa_schema(self):
        '''描述字段解释
        '''
        if schemacenter[self.name]:
            return pd.Series(schemacenter[self.name].property)
        return

    def pa_add_schema(self, params, replace=False):
        '''增加字段的说明等等，尤其是sql语句中新拉出来的特征
        param: 单个特征描述用{}
        '''
        if 'name' not in params:
            params['name'] = self.name
        schemacenter.pa_add_schema(params, replace)
    
    def pa_feature_transform(self, method='default', verbose=1, **params):
        '''对特征进行转换处理
        :param method: 支持转换的方式(可传入str或者function), 
                       'default', 'date2days', 'date2weeks', 'date2months', 'date2years', 'num2date'
        '''
        if isfunction(method):
            return method(self)

        if method == 'default':
            # 如果schema中有对应的处理方式，则默认使用
            if schemacenter[self.name] and schemacenter[self.name].transform:
                method = schemacenter[self.name].transform.split(',')[0]
                if verbose != 0:
                    print(f'[Info] Found and using {method} transform in schema')
            else:
                return self
        
        elif method in {'num2date'}:
            # 把int, float, str转换为datetime格式
            X = self.copy()
            X.name = self.name + f'_{method}'
            sel_index = ~self.isna()
            X[~sel_index] = np.nan  # 空余部分置为nan
            
            # float类型需要先转int
            if is_dtype_float(X):
                sel_series = X.loc[sel_index].astype('int')
            else:
                sel_series = X.loc[sel_index]

            X[sel_index] = pd.to_datetime(sel_series.astype('str'), errors='coerce')
            return X

        elif method in {'date2days', 'date2weeks', 'date2months', 'date2years'}:
            X = self.copy()
            X.name = self.name + f'_{method}'
            sel_index = ~self.isna()
            X[~sel_index] = np.nan  # 空余部分置为nan
            
            # 计算距今时间，float类型需要先转int
            if is_dtype_float(X):
                sel_series = X.loc[sel_index].astype('int')
            else:
                sel_series = X.loc[sel_index]
            
            # 允许传入end_dt
            end_date = params.get('dt', None)
            end_date = end_date if end_date else datetime.datetime.now()

            X[sel_index] = (end_date - pd.to_datetime(sel_series.astype('str'), errors='coerce')).dt.days
            if method == 'date2weeks':
                X[sel_index] = X[sel_index] / 7
            elif method == 'date2months':
                X[sel_index] = X[sel_index] / 30
            elif method == 'date2years':
                X[sel_index] = X[sel_index] / 365
            return X

        return self
    
    def pa_convert_dtypes(self):
        '''依据feature.xlsx中维护的字段类型，对series进行类型转换
        '''

        if schemacenter[self.name]:
            dtype = schemacenter[self.name].dtype
            if (dtype=='str') and (self.dtype!='O'):
                self_new = self.astype(str)  # 其中nan或者None会转成字符串
                self_new.loc[self.isna()] = np.nan
            elif is_dtype_float(dtype) and not is_dtype_float(self.dtype):
                self_new = self.astype(float)
            elif (dtype=='date') and (self.dtype=='O'):
                # 这里date默认转成数值型，方便后面分箱来做分析
                tmp = self.str.extractall(r'([0-9]+)').unstack()
                if len(tmp.columns)>=1:
                    self_new =  tmp[tmp.columns[0]]
                    for col in tmp.columns[1:]:
                        self_new += tmp[col]
                    self_new = self_new.astype(float)
        return self_new if 'self_new' in vars().keys() else self
