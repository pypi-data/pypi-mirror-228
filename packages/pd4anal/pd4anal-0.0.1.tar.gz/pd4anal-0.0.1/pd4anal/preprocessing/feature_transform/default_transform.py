from sklearn.preprocessing import StandardScaler, MinMaxScaler

class DefaultTransform(object):
    def __init__(self, name='default_preprocess', default_encode='raw', feature_list=[], specific_encode={}, **params):
        '''连续变量处理
        dense_default_encode:  编码方式
            raw: 不作处理
            std_scale: StandardScaler
            min_max_scale: MinMaxScaler()
        dense_list: 需要处理的特征列表
        dense_specific_encode: 单独为每个特征指定编码类型
        return_encoder：返回训练后的encoder
        '''
        self.name = name
        self.default_encode=default_encode
        self.feature_list = feature_list
        self.specific_encode = specific_encode
        self.encoder = dict()
    
    def fit(self, X, y=None, **tracker):
        self.feature_list += [i for i in tracker.get('dense_list', []) if i not in self.feature_list]
        self.feature_list += [i for i in self.specific_encode.keys() if i not in self.feature_list]

        for col in self.feature_list:
            choice = self.specific_encode.get(col, self.default_encode)
            if choice == 'raw':
                continue
            elif choice == 'std_scale':
                stdsc = StandardScaler()
                X[col] = stdsc.fit_transform(X[[col]])
                self.encoder[col] = stdsc
            elif choice == 'min_max_scale':
                stdsc = MinMaxScaler()
                X[col] = stdsc.fit_transform(X[[col]])
                self.encoder[col] = stdsc
            elif choice == 'qcut':
                pass
            elif choice == 'cut':
                pass
            else:
                raise ValueError(f'illegal choice={choice}')

        tracker['dense_list'] = self.feature_list
        return X, y, tracker
    
    def predict(self, df):
        pass
