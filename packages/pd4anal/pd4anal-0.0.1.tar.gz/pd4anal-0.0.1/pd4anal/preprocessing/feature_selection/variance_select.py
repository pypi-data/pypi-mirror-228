from collections import OrderedDict
import numpy as np
import pandas as pd


class VarianceFeatureSelect(object):
    '''按照方差进行排序，这里只能计算连续值的
    '''
    def __init__(self, name='variance_feature_select', topk=1000, bin_count=10, use_ratio=True, **kwargs):
        super().__init__()
        self.name = name
        self.pipeline_return = False
        self.topk = topk
        self.use_ratio = use_ratio
        self.bin_count = bin_count

    def fit(self, df_X, df_y=None, **tracker):        
        res = dict()
        for col in df_X.columns:
            # object类型手动计算
            if df_X[col].dtype == 'O':
                df_cnt = df_X.groupby(col).size()
                if self.use_ratio:
                    df_cnt = df_cnt / (~df_X[col].isna()).sum()
                res[col] = df_cnt.var()
            # 连续型变量
            else:
                if self.bin_count:
                    tmp = pd.qcut(df_X[col], q=self.bin_count, duplicates='drop', retbins=True)[0]
                    df_cnt = df_X.groupby(tmp).size()
                    if self.use_ratio:
                        df_cnt = df_cnt / (~df_X[col].isna()).sum()
                    res[col] = df_cnt.var()
                else:
                    res[col] = df_X[col].var()
        res = [(i, np.float64(v)) for i, v in res.items()]
        res = OrderedDict(sorted(res, key=lambda x: abs(x[1]), reverse=True)[:self.topk])

        if self.pipeline_return:
            tracker['entropy_map'] = res
            return df_X, df_y, tracker
        else:
            return res
