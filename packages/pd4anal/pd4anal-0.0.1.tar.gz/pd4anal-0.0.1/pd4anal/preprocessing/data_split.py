# 数据拆分
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit, train_test_split

class DataSplit(object):
    def __init__(self, name='data_split', method='train_test_split', split_options={'test_size': 0.2}, return_dataframe=False, **kwargs):
        '''数据切分
        
        :param tgt_name: 目标特征名
        :param method: 可选'train_test_split', 'StratifiedKFold', 'StratifiedShuffleSplit'
        :param split_options: 切分用到的参数
        :param return_dataframe: 是否返回切分后的dataframe，若为True则只返回切分的index
        '''
        self.name = name
        self.mode = method
        self.split_options = split_options
        self.pipeline_return = False
        self.return_dataframe = return_dataframe  # 放回dataframe

    def fit(self, X_data, y_data, **tracker):
        '''train和valid/dev的切分
        '''
        kfold = []
        if self.mode == 'train_test_split':
            # 随机抽样
            train_idx, valid_idx = train_test_split(range(len(X_data)), **self.split_options)
            kfold = [(train_idx, valid_idx)]
        elif self.mode == 'StratifiedKFold':
            # 交叉验证
            self.split_options['shuffle'] = True
            kfold = StratifiedKFold(**self.split_options).split(X_data, y_data)
        elif self.mode == 'StratifiedShuffleSplit':
            # 分层抽样
            kfold = StratifiedShuffleSplit(**self.split_options).split(X_data, y_data)
        else:
            raise ValueError(f'Args data_split {self.mode} not supported')
        tracker['kfold'] = kfold

        if self.pipeline_return:
            return X_data, y_data, tracker
        elif self.return_dataframe:
            res = [(X_data.loc[train_idx], y_data.loc[train_idx], X_data.loc[valid_idx], y_data.loc[valid_idx]) for train_idx, valid_idx in kfold]
            return res[0] if len(res) == 1 else res
        else:
            return kfold[0] if len(kfold) == 1 else kfold
