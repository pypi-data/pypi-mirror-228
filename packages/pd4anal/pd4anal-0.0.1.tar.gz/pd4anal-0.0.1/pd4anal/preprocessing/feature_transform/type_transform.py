import traceback

class TypeTransform(object):
    def __init__(self, skip_fea_list=[], name='type_preprocess', **params):
        '''根据变量类型确认离散和连续型变量
        sparse_list：如果列是object类型，且不是list格式的
        varlen_sparse_list：如果列是object类型，且不是list格式的
        dense_list：列是连续类型的
        '''
        self.name = name
        self.sparse_list = []
        self.dense_list = []
        self.varlen_sparse_list = []
        self.skip_list = set(skip_fea_list) if isinstance(skip_fea_list, (tuple, list)) else {skip_fea_list}

    def fit(self, X, y=None, **tracker):
        for col in X.columns:
            if col in self.skip_list:
                continue

            if X[col].dtype == 'O':
                try:
                    if isinstance(X[col].iloc[0], (tuple, list)):
                        self.varlen_sparse_list.append(col)
                        continue
                except:
                    print(traceback.format_exc())
                self.sparse_list.append(col)
            else:
                self.dense_list.append(col)      
        tracker.update({'sparse_list': self.sparse_list, 
                        'dense_list': self.dense_list, 
                        'varlen_sparse_list': self.varlen_sparse_list})
        return X, y, tracker
    
    def predict(self, X):
        return X
