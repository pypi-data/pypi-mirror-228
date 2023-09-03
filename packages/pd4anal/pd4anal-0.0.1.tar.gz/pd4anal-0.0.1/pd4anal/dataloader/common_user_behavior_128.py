'''
润华二级页面用户行为，从wia_robot.uba_kycd_userid_sclass128取数
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os
import pandas as pd


class UserBehavior128Loader(DataLoader):
    '''加载用户行为特征, 二级页面128维（目前用到60维）
    '''
    def __init__(self, source_um, pri_key='user_id') -> None:
        super().__init__(source_um, pri_key, sheet_name='user_behavior_128')


UserBehaviorLoader = UserBehavior128Loader  # 兼容旧代码
