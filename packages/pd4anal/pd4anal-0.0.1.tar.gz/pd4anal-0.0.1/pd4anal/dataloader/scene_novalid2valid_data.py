from .base import DataLoader
import warnings
from ..data.frame import DataFrame
import yaml
import os
from .common_user_bic import UserDataLoader
from .common_user_reg_info import UserRegInfoLoader
from .common_user_behavior_15 import UserBehavior15Loader
from .base import merge_features, datatools_fetch
import pandas as pd
import datetime


class Novalid2ValidLoader(DataLoader):
    '''加载(用户, 基金)特征
    '''
    def __init__(self, source_um) -> None:
        self.user = UserDataLoader(source_um, pri_key='cust_code')
        self.reg = UserRegInfoLoader(source_um, pri_key='cust_code')
        self.behavior = UserBehavior15Loader(source_um)
        self.features = merge_features(self.user.features, self.reg.features, self.behavior.features)  # 合并两者

    def load(self, dt, target_sql, user_feature_list=None, reg_feature_list=None, behavior_feature_list=None, label_day=None, verbose=0):
        '''
        dt: 获取数据的日期，examples: 20221114, '20221114', [20221113, 20221114]
        target_sql: 取用y的sql, 至少包含两列[user_name, 'dt']
        '''

        # bic用户维度
        if user_feature_list is None:
            user_feature_list = ['cust_code', 'channel_source_name', 'userid', 'open_date', 'gender', 'edu', 'marry', 'fee_ratio', 'rating_lvl',
                                 'bi_income', 'age', 'aum', 'login_count_1m_sum', 'bank_aum', 'interbank_min_mkt_amt', 'gender', 'edu', 'marry', 
                                 'fee_ratio', 'rating_lvl', 'age', 'aum', 'login_count_1m_sum', 'bank_aum']
        user_data = self.user.load(dt, target_sql, join_on='cust_code', feature_list=user_feature_list, verbose=verbose)
        print(f'Load {user_data.shape[0]} user_data')

        # 注册大底表
        if reg_feature_list is None:
            reg_feature_list = ['cust_code', 'telephone_area', 'usersource', 'device_id', 'unify_aid', 'unify_sid', 'before_kh_ouid', 'register_hdid', 
                                'hk_channel_1nd', 'hk_channel_2nd', 'group_actual_amt', 'zd_age_stock_v3', 'ajj_kh_flag', 'otp_flag', 'dd_aid']
        reg_data = self.reg.load(dt, target_sql, join_on='cust_code', feature_list=reg_feature_list, verbose=verbose)
        print(f'Load {reg_data.shape[0]} reg_data')

        # 15维的行为数据
        if behavior_feature_list is None:
            behavior_feature_list = ['cust_code', 'fund','home','ia','im','ipo','live','news','other','personal','price','promotion','search','sim_trade',
                                     'trade','unknown','lesson']
        behavior_data = self.behavior.load(dt, target_sql, join_on='cust_code', feature_list=behavior_feature_list, verbose=verbose)
        print(f'Load {behavior_data.shape[0]} behavior_data')

        # 合并
        user_data['cust_code'] = user_data['cust_code'].map(int)
        reg_data['cust_code'] = reg_data['cust_code'].map(int)
        df = pd.merge(user_data, reg_data[reg_feature_list], how='left', on=['cust_code'])
        del reg_data

        behavior_data['cust_code'] = behavior_data['cust_code'].map(int)
        df = pd.merge(df, behavior_data[behavior_feature_list], how='left', on=['cust_code'])
        del behavior_data
        
        # 后处理
        df['dt'] = dt
        df['dt_'] = df['dt'].map(lambda x: datetime.datetime.strptime(str(int(x)),'%Y%m%d'))
        if label_day is not None:
            SQL = f'''
            select cust_code, max(gyyxhsxr) as gyyxhsxr
            from fact.ui_index_module_cust_valid
            where dt={label_day}
            group by cust_code
            '''
            df_label = datatools_fetch(self.um, SQL)
            df_label['cust_code'] = df_label['cust_code'].map(int)
            df = pd.merge(df, df_label, how='left', on='cust_code')
            del df_label
            df['gyyxhsxr_'] = df['gyyxhsxr'].fillna(20291231).map(lambda x: datetime.datetime.strptime(str(int(x)),'%Y%m%d'))
            df['gyyxh_days'] = (df['gyyxhsxr_'] - df['dt_']).map(lambda x: max(x.days,0))
            df['y'] = df['gyyxh_days'].map(lambda x: 1 if x<=30 else 0)
        
        df['open_date_'] = df['open_date'].map(lambda x: datetime.datetime.strptime(str(int(x)),'%Y%m%d'))
        df['open_days'] = (df['dt_'] - df['open_date_']).map(lambda x: max(x.days,0))
        df['open_days_cut'] = pd.cut(df['open_days'], [-1, 7, 14, 30, 180, 360, 1e8], labels=False)

        # fillna
        for fea in behavior_feature_list:
            df[fea] = df[fea].fillna(0).map(float)
        for fea in ['age','fee_ratio']:
            df[fea] = df[fea].fillna(df[fea].mean())
        for fea in ['rating_lvl','channel_source_name','telephone_area','unify_aid', 'unify_sid', 'before_kh_ouid', 'register_hdid',
                    'gender','edu','marry', 'bi_income','usersource','hk_channel_1nd','hk_channel_2nd','group_actual_amt']:
            df[fea] = df[fea].fillna(-1)
        for fea in ['aum','login_count_1m_sum','bank_aum','interbank_min_mkt_amt','zd_age_stock_v3']:
            df[fea] = df[fea].fillna(0)
        df['flag_device'] = df['device_id'].map(lambda x: 1 if x else 0)
        df = df.fillna(-1)

        # train negative sample
        print('before df.shape',df.shape)
        if label_day is not None:
            df = pd.concat([df[df['y']>0], df[df['y']==0].sample(frac=0.35)], ignore_index=True)
        print('after df.shape', df.shape)
        print('merge_df done')

        return DataFrame(df)


if __name__ == '__main__':
    user = Novalid2ValidLoader()
    dt = 20221011
    target_sql = f'''select cust_code, channel_source_name, dt
                from fact.ui_index_module_cust_valid
                where dt={dt} and gyyxhsxr is null and length(cust_code)>0'''

    user.load(dt, target_sql)
