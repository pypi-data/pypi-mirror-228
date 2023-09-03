class NanTransform(object):
    def __init__(self, name='nan_preprocess', sparse_nan_fill='raw', dense_nan_fill='raw', sparse_list=[], 
                 dense_list=[], fill_values={}, inplace=False, **params):
        self.name = name
        self.sparse_nan_fill = sparse_nan_fill
        self.dense_nan_fill = dense_nan_fill
        self.sparse_fill = sparse_list
        self.dense_fill = dense_list
        self.fill_values = fill_values
        self.encoder = {}
        self.inplace = inplace

    def fit(self, X, **tracker):
        '''缺失值处理，nan的处理, 主要逻辑是填充固定值
        sparse_nan_fill: 离散值填充，'raw'表示不填充，也可以给定固定值填充
        dense_nan_fill： 连续值填充，'raw'表示不填充，'average'表示均值填充，也可以给定固定值填充
        '''
        df = X if self.inplace else X.copy()
        if isinstance(self.sparse_fill, list):
            self.sparse_fill = {col: self.fill_values[col] if col in self.fill_values else self.sparse_nan_fill for col in self.sparse_fill}
            # print(sparse_fill)
        if isinstance(self.dense_fill, list):
            self.dense_fill = {col: self.fill_values[col] if col in self.fill_values else self.dense_nan_fill for col in self.dense_fill}
            # print(dense_fill)
            
        # 离散值
        for col, val in self.sparse_fill.items():
            if val == 'raw':
                continue
            else:
                df[col] = df[col].fillna(val)
            self.encoder[col] = val
        # 连续值
        for col, val in self.dense_fill.items():
            if val == 'average':
                val = df[col].mean()
            elif val == 'raw':
                continue
            else:
                df[col] = df[col].fillna(val)
            self.encoder[col] = val
        return df, tracker
        
    def predict(self, X):
        for col, val in self.encoder:
            X[col] = X[col].fillna(val)
        return X

