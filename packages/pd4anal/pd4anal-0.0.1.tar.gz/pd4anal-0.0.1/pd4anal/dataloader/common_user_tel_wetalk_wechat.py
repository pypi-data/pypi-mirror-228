'''
客户触达的信息，含tel/wechat/wetalk
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime


class LocalBaseLoader(DataLoader):
    '''基类
    '''
    def __init__(self, source_um, pri_key='cust_code', sheet_name=None) -> None:
        super().__init__(source_um, pri_key, sheet_name=sheet_name)
    
    def gen_sql(self, dt, target_sql, pri_key_list, feature_list):
        '''
        '''
        self.filter_featurs(feature_list)

        # 如果是单独的dt，则默认统计过去一个月
        if isinstance(dt, (str, int)):
            dt_start = datetime.strptime(str(dt), '%Y%m%d')-relativedelta(months=1)
            dt_start = int(datetime.strftime(dt_start, '%Y%m%d'))
            dt = [dt_start, dt]
            warnings.warn(f'Args `dt` is str/int formart, and reset to {dt}, you can input dt=[dt_start, dt_end] instead')

        dt_str = self.get_dt_str(dt)

        if pri_key_list:
            SQL_part = f" and {self.pri_key} in ({', '.join(pri_key_list)})"
        else:
            SQL_part = ''

        SQL = self.adjust_sql(dt_str+SQL_part)

        return SQL
    
    def adjust_sql(self, where_sql):
        raise NotImplementedError


class UserTelephone(LocalBaseLoader):
    '''电销, 走CC系统
    '''
    def __init__(self, source_um, pri_key='cust_code') -> None:
        super().__init__(source_um, pri_key, sheet_name='telephone')

    def adjust_sql(self, where_sql):
        SQL = f'''select cust_code, sum(call_num_d) call_num_d, sum(conn_num_d) conn_num_d, sum(call_duration_d) call_duration_d,
        min(first_call_time) as first_call_time, min(first_conn_time) as first_conn_time
        from view.ADS_I_TEL_MARK_CONTACT where {where_sql}
        group by cust_code'''
        return SQL


class UserWetalk(LocalBaseLoader):
    '''Wetalk，呼叫不是直接端到端，而是中间有个中转，显示虚拟号
    '''
    def __init__(self, source_um, pri_key='cust_code') -> None:
        super().__init__(source_um, pri_key, sheet_name='wetalk')

    def adjust_sql(self, where_sql):
        SQL = f'''
        select cust_code, 
        sum(call_num_d) call_num_d, 
        sum(caller_num_d) caller_num_d,
        sum(called_num_d) called_num_d,
        sum(duration_d) duration_d,
        sum(caller_duration_d) caller_duration_d,
        min(first_call_time) first_call_time,
        min(first_conn_time) first_conn_time
        from view.ADS_i_WETALK_CONTACT where {where_sql}
        group by cust_code
        '''
        return SQL


class UserWechat(LocalBaseLoader):
    '''微信聊天
    '''
    def __init__(self, source_um, pri_key='cust_code') -> None:
        super().__init__(source_um, pri_key, sheet_name='wechat')

    def adjust_sql(self, where_sql):
        SQL = f'''
        select cust_code, 
        sum(if_act) if_act, 
        sum(if_connect) if_connect,
        sum(if_service) if_service,
        sum(ct_talk_cust_s_day) ct_talk_cust_s_day,
        sum(ct_talk_cust_g_day) ct_talk_cust_g_day,
        sum(ct_talk_cust_g_day1) ct_talk_cust_g_day1,
        min(first_join_date) first_join_date
        from view.ADS_A_WECHAT_CONTACT where {where_sql}
        group by cust_code
        '''
        return SQL
