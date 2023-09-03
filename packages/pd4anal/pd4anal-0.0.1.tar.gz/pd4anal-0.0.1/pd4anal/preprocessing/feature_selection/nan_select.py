from collections import OrderedDict


class NanFeatureSelect(object):
    '''按照缺失值进行排序
    '''
    def __init__(self, name='nan_feature_select', topk=1000, **kwargs):
        super().__init__()
        self.name = name
        self.pipeline_return = False
        self.topk = topk

    def fit(self, df_X, df_y=None, **tracker):
        nan_map = []
        for feature in df_X.columns:
            ratio = df_X[feature].isna().sum() / df_X.shape[0]
            nan_map.append((feature, ratio))
        nan_map = OrderedDict(sorted(nan_map, key= lambda x: x[1])[:self.topk])

        if self.pipeline_return:
            tracker['nan_map'] = nan_map
            return df_X, df_y, tracker
        else:
            return nan_map
