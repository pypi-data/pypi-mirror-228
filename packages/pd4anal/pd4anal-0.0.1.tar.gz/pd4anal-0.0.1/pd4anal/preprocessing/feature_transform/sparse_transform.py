from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np


class SparseTransform(object):
    def __init__(self, name='sparse_preprocess', sparse_encode='raw', sparse_list=[], sparse_specific_encode={}, 
                 inplace=False, tgt_name=None, **params):
        '''离散变量处理
        sparse_encode: 编码方式
            raw: 不作处理
            dummy: onehot编码
            label_encoder：直接映射到0,1,2,...
            dict_encoder：自己实现的label_encoder, 不依赖sklearn，且有default值
            dict: 和label_encoder类似，但是有顺序之分
            woe: woe编码
        fea_list: 需要处理的特征列表
        sparse_specific_encode: 单独为每个特征指定编码类型
        tgt_name：目标列，目前仅woe转码需要使用
        input_encoder：使用input_encoder进行转码
        return_encoder：返回训练后的encoder
        '''
        self.name = name
        self.default_encode = sparse_encode
        self.feature_list = sparse_list
        self.specific_encode = sparse_specific_encode
        self.tgt_name = tgt_name
        self.encoder = dict()
        self.inplace = inplace

    def fit(self, X, y=None, **tracker):
        df = X if self.inplace else X.copy()
        self.feature_list += [i for i in tracker.get('sparse_list', []) if i not in self.feature_list]
        self.feature_list += [i for i in self.specific_encode.keys() if i not in self.feature_list]

        for col in self.feature_list:
            # 自己编码
            choice = self.specific_encode.get(col, self.default_encode)
            if choice == 'raw':
                continue
            elif choice == 'dummy':
                data_dummy = pd.get_dummies(df[[col]], prefix=f'{col}_oh')
                df.drop(col, axis=1, inplace=True)
                df = df.join(data_dummy)
            elif choice == 'label_encoder':
                lbl = LabelEncoder()
                df[col] = lbl.fit_transform(df[col])  # .astype(str)
                self.encoder[col] = lbl
            elif choice == 'dict_encoder':
                lbl = DictEncoder()
                df[col] = lbl.fit_transform(df[col])
                self.encoder[col] = lbl
            elif choice == 'dict':
                # nan作key索引不到，转为'nan'，有的离散型是有顺序之分，因此排序下
                val_unique = df[col].unique()
                val_unique = [i for i in val_unique if (str(i) != 'nan') and (str(i) != 'None')]
                # 因为很多离散变量用数值表示，是有顺序概念的
                try:
                    val_unique = sorted(val_unique)
                except Exception as e:
                    print(e)
                    print(col, ' ----> ', val_unique[:10])
                val_unique = val_unique + ['nan']
                mapping = {v:i for i, v in enumerate(val_unique)}
                df[col] = df[col].fillna('nan')
                df[col] = df[col].map(mapping)
                self.encoder[col] = mapping
            elif choice == 'woe':
                # df[col] = df[col].fillna('nan')
                # mapping = proc_woe_discrete(df, self.tgt_name, col)
                # df[col] = df[col].map(mapping)
                # self.encoder[col] = mapping

                assert self.tgt_name is not None, 'Tgt_name can not be None when doing woe transform'
                woe = WoeEncoder()
                df[col] = woe.fit_transform(df, self.tgt_name, col)
                self.encoder[col] = woe
            else:
                raise ValueError(f'illegal choice={choice}')
        tracker['sparse_list'] = self.feature_list
        return df, tracker
    
    def predict(self, X):
        for col, trans in self.encoder.items():
            X[col] = trans.transform(X[col])
        return X

        
class DictEncoder():
    '''labelEncoder的实现，不依赖sklearn且可以增加default默认值，来表示不在字典中的项目
    '''
    def __init__(self, mapping=None):
        self.mapping = mapping
        
    def fit_transform(self, df_series, default=None):
        self.mapping = {v:i for i, v in enumerate(df_series.unique())}
        if default:
            self.mapping.update(self.mapping.get(default, max(self.mapping.values)+1))
        return df_series.map(self.mapping)
    
    def transform(self, val):
        if isinstance(val, (list, tuple)):
            return [self.mapping[i] for i in val]
        else:
            return self.mapping[val]
    
    @property
    def classes_(self):
        return self.mapping


class WoeEncoder():
    '''woe的encoder
    作用和proc_woe_discrete一样，只是包装了fit_tranform和transform方法，在predict时候可以统一使用transform接口
    '''
    def __init__(self, mapping=None):
        self.mapping = mapping
        
    def fit_transform(self, xdf, tgt, var, eps=1e-5, return_iv=False):
        self.mapping = proc_woe_discrete(xdf, tgt, var)
        return xdf[var].map(self.mapping)
        
    def transform(self, series):
        return series.map(self.mapping)


def proc_woe_discrete(xdf, tgt, var, eps=1e-5, return_iv=False):
    '''计算变量的woe值
      xdf: 输入的dataframe
      tgt: 目标y的name
      var: 特征x的name
    '''
    # 整体正负样本比
    total_good = xdf[tgt].sum()
    total_bad = xdf[tgt].count()-total_good
    totalRate = total_good / total_bad

    msheet = xdf[[tgt, var]]
    grouped = msheet.groupby(var)
        
    groupGood = grouped.sum()[tgt]
    groupTotal = grouped.count()[tgt]
    groupBad = groupTotal - groupGood
    groupRate = (groupGood+eps)/(groupBad+eps)
    woe = np.log(groupRate/totalRate)
    if return_iv:
        iv = np.sum((groupGood/total_good-groupBad/total_bad)*woe)
        return woe.to_dict(), iv
    else:
        return woe.to_dict()
