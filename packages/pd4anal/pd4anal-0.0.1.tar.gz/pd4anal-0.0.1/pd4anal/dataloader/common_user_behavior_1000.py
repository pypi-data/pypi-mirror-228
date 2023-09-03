'''
润华1000维用户行为分
'''
from .base import DataLoader
import warnings
from ..data import DataFrame, schemacenter
import yaml
import os
import pandas as pd


class UserBehavior1000Loader(DataLoader):
    '''加载用户行为特征，1000维度的
    '''
    def __init__(self, source_um, pri_key='device_code') -> None:
        super().__init__(source_um, pri_key, sheet_name='use_behavior_1000')

