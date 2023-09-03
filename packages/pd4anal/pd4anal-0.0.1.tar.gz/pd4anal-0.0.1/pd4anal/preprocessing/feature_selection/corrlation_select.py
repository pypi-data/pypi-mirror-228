from sklearn.preprocessing import LabelEncoder
import numpy as np
from collections import OrderedDict


class CorrlationFeatureSelect(object):
    '''按照自变量相关性进行排序
    '''
    def __init__(self, name='corrlation_feature_select', topk=1000, dense_only=True, **kwargs):
        super().__init__()
        self.name = name
        self.pipeline_return = False
        self.topk = topk
        self.dense_only = dense_only  # 只计算dense变量的

    def fit(self, df_X, df_y=None, **tracker):
        dense_feat = [col for col in df_X.columns if df_X[col].dtype != 'O']
        df = df_X[dense_feat].copy() if self.dense_only else df_X.copy()
        
        # object类型要label_encoder下
        for col in df.columns:
            if df[col].dtype == 'O':
                lbl = LabelEncoder()
                try:
                    df[col] = lbl.fit_transform(df[col])
                except TypeError:
                    df[col] = lbl.fit_transform(df[col].astype(str))
        
        # ========================没有y计算两两配对的相关系数========================
        if df_y is None:
            corrmat = df.corr()
            # 计算相关系数最大的特征对
            corr_dict = corrmat.abs().sum().to_dict()
            res = dict()
            for k in corrmat.columns:
                for j in corrmat.columns:
                    if (k == j) or ((k, j) in res) or ((j, k) in res):
                        continue
                    elif corr_dict[j] > corr_dict[k]:  # j的相关系数和更大
                        res[(k, j)] = corrmat.loc[k, j]
                    elif corr_dict[j] < corr_dict[k]:  # k的相关系数和更大
                        res[(j, k)] = corrmat.loc[j, k]
            # 需要丢弃的是后一个数值
            res = [(i, np.float64(v)) for i, v in res.items()]
            res = OrderedDict(sorted(res, key=lambda x: abs(x[1]), reverse=True)[:self.topk])
            print('[INFO] The latter feature in {previous, `latter`} can be dropped')
        
        # ========================有y且为数值型========================
        elif (df_y.dtype == float) or (df_y.dtype == int):
            res = dict()
            for col in df.columns:
                if col == df_y.name:
                    continue
                elif (df[col].dtype != float) and (df[col].dtype != int):
                    continue
                else:
                    res[col] = df[col].corr(df_y)
            res = [(i, np.float64(v)) for i, v in res.items()]
            res = OrderedDict(sorted(res, key=lambda x: abs(x[1]), reverse=True)[:self.topk])

        # ========================有y但不是数值型，无法计算相关系数========================
        else:
            print(f'[WARN] Args tgt_name=`{df_y.name}` is not a numeric feature')
            return None

        if self.pipeline_return:
            return df_X, df_y, tracker
        else:
            return res
        
