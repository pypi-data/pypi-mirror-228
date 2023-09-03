# 绘图功能区域
import seaborn as sns
import math
import warnings
from collections import OrderedDict
import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np
import pandas as pd
import os
import traceback
from ..data.schema import schemacenter
from .base import LineChartPercentBase


class LineChartPercentHue(LineChartPercentBase):
    def __init__(self, name='line_chart_percent_hue', hue=None, **kwargs):
        '''LineChartPercent的多维版，如按“获客渠道”来分，看不同渠道的客户在不同“资产分层”上“目标客户的占比”
        args:
            hue: 按照某个特征列拆分来绘制柱状图、对应的折线图，即多条折线，多个柱形图，默认为None
        '''
        super().__init__(**kwargs)
        self.name = name
        self.hue = hue
        assert hue is not None, 'Args `hue` can not be None'


    def trans_df(self, df_X, df_y):
        df, tgt_name = super().trans_df(df_X, df_y)  # 合并df
        if (df[tgt_name].nunique() > 2) and (self.hue is not None):
            raise ValueError('Multi class target and not none args `hue` can not exists at the same time')
        assert self.hue in df.columns, 'Args `hue` should be in df columns'
        return df, tgt_name

    def process_sparse(self):
        '''处理离散变量
        '''
        df_sort = self.df_del.groupby(self.fea)[self.tgt_name].mean().sort_values()  # 排序一下，和line_chart_percent_hue保持一致
        df_plt = self.df_del.groupby([self.fea, self.hue])[self.tgt_name].mean().unstack()
        df_plt = df_plt.loc[df_sort.index]
        df_cnt = self.df_del.groupby([self.fea, self.hue])[self.tgt_name].count().reset_index()
        return df_plt, df_cnt

    def process_dense(self):
        '''处理连续变量
        '''
        # 二分类
        __fea = '__' + self.fea
        df_plt = self.df.groupby([__fea, self.hue])[self.tgt_name].mean().unstack()
        df_cnt = self.df.groupby([__fea, self.hue])[self.tgt_name].count().reset_index()
        return df_plt, df_cnt
    
    def plot_left(self):
        # 绘制客户占比折线图
        self.df_plt.fillna(0, inplace=True)
        for col in self.df_plt.columns:
            self.ax1.plot(self.xticks, self.df_plt[col].values)
        # legend
        self.ax1.legend(self.get_left_legend(), loc='upper left')

    def plot_right(self):
        __fea = '__' + self.fea
        x = __fea if self.fea in self.dense_list else self.fea
        sns.barplot(data=self.df_cnt, x=x, hue=self.hue, y=self.tgt_name, alpha=self.alpha, ax=self.ax2, order=self.df_plt.index)
        self.ax2.set_xticklabels(labels=self.xticks, rotation=self.rotation, horizontalalignment=self.horizontalalignment)
        self.ax2.legend(loc='upper right')

