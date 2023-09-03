from collections import OrderedDict
import numpy as np
import pandas as pd

class EntropyFeatureSelect(object):
    '''按照信息熵进行排序
    '''
    def __init__(self, name='entropy_feature_select', topk=1000, bin_count=10, use_entropy_estimators=False, continuous_mode='get_h_mvn', fillna=False, **kwargs):
        super().__init__()
        self.name = name
        self.pipeline_return = False
        self.topk = topk
        
        self.bin_count = bin_count
        self.use_entropy_estimators = use_entropy_estimators
        assert continuous_mode in {'get_h_mvn', 'get_h'}
        self.continuous_mode = continuous_mode
        self.continuous_k = kwargs.get('continuous_k', 5)
        self.fillna = fillna

    def fit(self, df_X, df_y=None, **tracker):
        if self.use_entropy_estimators:
            from entropy_estimators import continuous

        df = df_X.copy()
        
        res = dict()
        for col in df.columns:
            # object类型手动计算
            if df[col].dtype == 'O':
                if self.fillna:
                    df[col] = df[col].fillna('nan')
                a = df[col].value_counts() / (~df[col].isna()).sum()
                assert sum(a)-1 < 1e-3
                res[col] = sum(np.log2(a) * (-a))
            
            elif self.use_entropy_estimators:
                # 连续型变量使用entropy_estimators包计算
                if self.continuous_mode == 'get_h_mvn':
                    res[col] = continuous.get_h_mvn(df[col])
                elif self.continuous_mode == 'get_h':
                    res[col] = continuous.get_h(df[col], k=self.continuous_k)
                else:
                    raise ValueError(f'Col {col} can not be identified')
            else:
                if self.fillna:
                    fill_value = df[col].min() - df[col].max()
                    df[col] = df[col].fillna(fill_value).map(float)

                tmp = pd.cut(df[col], bins=self.bin_count)  # 这里只能用cut而不能用qcut
                df_cnt = df.groupby(tmp).size()
                a = df_cnt / (~df[col].isna()).sum()
                a = a[a>0]
                assert sum(a)-1 < 1e-3
                res[col] = sum(np.log2(a) * (-a))

        res = [(i, np.float64(v)) for i, v in res.items()]
        res = OrderedDict(sorted(res, key=lambda x: abs(x[1]), reverse=True)[:self.topk])

        if self.pipeline_return:
            tracker['entropy_map'] = res
            return df_X, df_y, tracker
        else:
            return res
