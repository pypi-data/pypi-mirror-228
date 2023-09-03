import pandas as pd
import numpy as np
from collections import OrderedDict
import warnings
import os
import json
from tqdm import tqdm
from pd4anal.utils import is_dtype_numberic


def cal_iv(df_X, df_y, col_name, sparse_flag=True, bin_count=10, bins=None, eps=1e-5, dense_fill='default'):
    '''计算某个指标的iv, 多分类计算的时候转化为多个二分类来计算
    '''
    def cal_iv_2category(tmp, df_y):
        gbi = pd.crosstab(tmp, df_y) + eps
        # gb = df_y.value_counts() + eps   # 旧逻辑，这样作为分母的文字是gbi计算是不含nan的，但是df_y是含nan的
        gb = gbi.sum()  # 新逻辑，直接使用gbi的口径，这样分子分母的逻辑是统一的
        gbri = gbi / gb
        if gbri.shape[1] != 2:
            # 由于去除nan来计算iv值，因此可能会遇到只有一列，这里需要单独处理一下
            warnings.warn(f"Feature {col_name}'s target categories={gbri.shape[1]} not 2")
            return -1
        y0 = gbri.columns[0]
        y1 = gbri.columns[1]
        gbri['woe'] = np.log(gbri[y1] / gbri[y0])
        gbri['iv'] = (gbri[y1] - gbri[y0]) * gbri['woe']
        return gbri['iv'].sum()

    if sparse_flag:
        tmp = df_X[col_name].map(str)  # 这里nan也会变成'nan'
    else:
        if dense_fill == 'default':
            tmp = df_X[col_name].map(float)
        elif dense_fill == 'min-max':  # 缺失值用最小值-最大值来填充，希望单独成桶
            fill_value = df_X[col_name].min() - max(999, df_X[col_name].max())
            tmp = df_X[col_name].fillna(fill_value).map(float)
        else:
            raise ValueError('Args `dense_fill` only support `default` and `min-max`')

        if bins is None:  # 按照qcut切分
            tmp = pd.qcut(tmp,q=bin_count, duplicates='drop')
        else:  # 按照cut切分
            tmp = pd.cut(tmp, bins, duplicates='drop')
    
    if df_y.nunique() > 2:
        iv_sum = 0
        for catetory in df_y.unique():
            iv_sum += cal_iv_2category(tmp, (df_y==catetory).astype(int))
        return iv_sum / df_y.nunique()
    else:
        return cal_iv_2category(tmp, df_y)

class IvFeatureSelect(object):
    '''计算各个特征X排序后的iv值
    '''
    def __init__(self, name='iv_feature_select', sparse_list=[], dense_list=[], 
                 bin_count=10, topk=1000, bins=None, dense_fill='default', save_path=None, **kwargs):
        super().__init__()
        self.name = name
        self.bin_count = bin_count
        self.sparse_list = sparse_list
        self.dense_list = dense_list
        self.pipeline_return = False
        self.topk = topk
        self.bins = bins or {}
        self.dense_fill = dense_fill
        self.save_path = save_path

    def fit(self, df_X, df_y, **tracker):
        if self.save_path is not None:
            # 创建文件夹
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            # 从本地文件恢复
            if os.path.exists(self.save_path):
                print(f'[INFO] resume iv json data from local cached file: {self.save_path}')
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    return json.load(f)

        self.sparse_list += [i for i in tracker.get('sparse_list', []) if i not in self.sparse_list]
        self.dense_list += [i for i in tracker.get('dense_list', []) if i not in self.dense_list]

        # 如果均为空，则默认使用df_X的字段类型来判断
        if len(self.sparse_list) + len(self.dense_list) == 0:
            self.dense_list = [col for col in df_X.columns if is_dtype_numberic(df_X[col])]
            self.sparse_list = [col for col in df_X.columns if col not in self.dense_list]

        # ================计算iv================
        iv_importance = []
        # 离散变量：缺失值当成单独的nan来处理
        for fea in tqdm(self.sparse_list, desc='Caculating sparse features'):
            score = cal_iv(df_X, df_y, col_name=fea, sparse_flag=True)
            iv_importance.append((fea, score))
        # 连续变量：提供了bins分段的按照bins分段来切分，未提供的按照默认bin_count来分段，nan默认是不处理
        for fea in tqdm(self.dense_list, desc='Caculating dense features'):
            bins = self.bins.get(fea, None)
            score = cal_iv(df_X, df_y, col_name=fea, sparse_flag=False, bin_count=self.bin_count, bins=bins, dense_fill=self.dense_fill)
            iv_importance.append((fea, score))
        iv_importance =  OrderedDict(sorted(iv_importance, key=lambda x: x[1], reverse=True)[:self.topk])
        
        # 保存文件到本地
        if self.save_path is not None:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(iv_importance, f, indent=4, ensure_ascii=False)
            print(f'[INFO] save iv json data to local cached file: {self.save_path}')

        if self.pipeline_return:
            return df_X, df_y, tracker
        else:
            return iv_importance

