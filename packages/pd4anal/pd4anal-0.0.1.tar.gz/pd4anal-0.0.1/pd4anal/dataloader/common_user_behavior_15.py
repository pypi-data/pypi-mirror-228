'''
润华15维用户行为分
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os
import pandas as pd


class UserBehavior15Loader(DataLoader):
    '''加载用户行为特征，15维度的
    '''
    def __init__(self, source_um, pri_key='cust_code') -> None:
        super().__init__(source_um, pri_key, sheet_name='user_behavior_15')

