from .common_user_bic import UserDataLoader
from .common_user_reg_info import UserRegInfoLoader
from .common_user_behavior_128 import UserBehavior128Loader
from .base import DataLoader, merge_features
from ..data import DataFrame, schemacenter
import pandas as pd
import os


class UserDataRegBehaviorLoader(DataLoader):
    '''加载用户bic特征 + reg底表 + 二级页面行为分
    '''
    def __init__(self, source_um, use_reg=True, use_behavior=True) -> None:
        self.user = UserDataLoader(source_um)
        self.reg = UserRegInfoLoader(source_um)
        self.behavior = UserBehavior128Loader(source_um)
        self.features = merge_features(self.user.features, self.reg.features, self.behavior.features)  # 合并两者
        self.use_behavior = use_behavior  # 这张表比较新，因此控制
        self.use_reg = use_reg

    def load(self, dt, target_sql, join_on='userid', join_on_dt=False, user_list=None, feature_list=None, how='inner', convert_dtypes=True, 
             verbose=0, save_path=None):
        '''
        dt: 获取数据的日期，examples: 20221114, '20221114', [20221113, 20221114]
        target_sql: 取用y的sql, 至少包含两列[user_name, 'dt']
        '''
        if dt < 20220731:
            self.use_behavior = False
            print('[WARNING] behavior table start from 20220731')
        if dt < 20220328:
            self.use_reg = False
            print('[WARNING] reg table start from 20220328')
        cache_dir = os.path.dirname(save_path)

        # bic用户维度
        save_path = os.path.join(cache_dir, f'bic_data_{dt}.pkl')
        print('Get bic data from hive')
        bic_data = self.user.load(dt, target_sql, join_on=join_on, how=how, feature_list=feature_list, convert_dtypes=convert_dtypes, 
                                  verbose=verbose, save_path=save_path)
        print(f'Load {bic_data.shape[0]} bic_data')

        # 注册大底表
        if self.use_reg:
            save_path = os.path.join(cache_dir, f'reg_data_{dt}.pkl')
            print('Get reg data from hive')
            reg_data = self.reg.load(dt, target_sql, join_on=join_on, how=how, feature_list=feature_list, convert_dtypes=convert_dtypes, verbose=verbose)
            print(f'Load {reg_data.shape[0]} reg_data')

        # 行为数据
        if self.use_behavior:
            save_path = os.path.join(cache_dir, f'behavior_data_{dt}.pkl')
            print('Get behavior data from hive')
            behavior_data = self.behavior.load(dt, target_sql, join_on=join_on, how=how, feature_list=feature_list, convert_dtypes=convert_dtypes, verbose=verbose)
            behavior_data.to_pickle(save_path)
            print(f'Load {behavior_data.shape[0]} behavior_data')
        
        # merge data
        df = bic_data
        if self.use_reg:
            merge_cols = [col for col in reg_data.columns if col not in df.columns]
            df = pd.merge(df, reg_data[[join_on]+merge_cols], how='left', on=[join_on])
        if self.use_behavior:
            merge_cols = [col for col in behavior_data.columns if col not in df.columns]
            df = pd.merge(df, behavior_data[[join_on] + merge_cols], how='left', on=[join_on])

        # 删除文件
        for file_path in [f'bic_data_{dt}.pkl', f'reg_data_{dt}.pkl', f'behavior_data_{dt}.pkl']:
            save_path = os.path.join(cache_dir, file_path)
            if os.path.exists(save_path):
                os.remove(save_path)

        df = DataFrame(df)
        # 保存文件到本地
        if save_path is not None:
            data.to_pickle(save_path)

        return df
