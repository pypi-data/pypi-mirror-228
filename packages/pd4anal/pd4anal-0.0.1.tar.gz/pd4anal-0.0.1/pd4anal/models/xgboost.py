import xgboost
from .base import Model
import numpy as np
from collections import OrderedDict
from ..evaluator.feature_importance import TreeFeatureImportance, TreeShapFeatureImportance

class XGBClassifier(xgboost.XGBClassifier, Model):
    def feature_importance(self, X, y, method='tree', save_path=None, **params):
        if method == 'tree':
            importance_ = TreeFeatureImportance(**params)
        elif method == 'shap':
            importance_ = TreeShapFeatureImportance(**params)
        else:
            raise ValueError(f'Method `{method}` is not supported')

        importance_.fit(X, y, model=[self])
        if len(importance_.feature_importance) == 1:
            return importance_.feature_importance[0]
        else:
            return importance_.feature_importance
    
    def predict(self, *args, probas=True, **kwargs):
        if probas:
            return super().predict_proba(*args, **kwargs)
        else:
            return super().predict(*args, **kwargs)
