import pandas as pd
import numpy as np
from collections import OrderedDict


def gather_dummy_fea(fea_importance, sparse_list, sparse_default_encode='dummy', dummy_fea_gather='average'):
    '''对于onehot的变量，其特征重要性计算
    '''
    if sparse_default_encode == 'dummy':
        new_feature_importace = dict()
        for fea, value in fea_importance.items():
            fea = fea.split('_oh_')[0]
            if fea in sparse_list:
                new_feature_importace[fea] = new_feature_importace.get(fea, []) + [value]            
            else:
                new_feature_importace[fea] = value
        for k, v in new_feature_importace.items():
            if isinstance(v, list):
                if dummy_fea_gather == 'average':
                    new_feature_importace[k] = np.mean(v)
                elif dummy_fea_gather == 'percentile':
                    new_feature_importace[k] = np.percentile(v, 50)
        fea_importance = [(k, abs(v)) for k, v in new_feature_importace.items()]
        fea_importance = OrderedDict(sorted(fea_importance, key=lambda x: x[1], reverse=True))
    return fea_importance
