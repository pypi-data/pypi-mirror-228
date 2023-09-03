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


class LineChartPercent(LineChartPercentBase):
    def __init__(self, name='line_chart_percent', **kwargs):
        '''根据传入的df的tgt_name，绘制依据特征x分布的各类客户占比图、客户频数分布直方图，纵轴为tgt_name中正例占比，其中tgt_name支持多个分类
        '''
        super().__init__(**kwargs)
        self.name = name

    def trans_df(self, df_X, df_y):
        df, tgt_name = super().trans_df(df_X, df_y)  # 合并df
        self.multi_class = df[tgt_name].nunique() > 2
        self.avg_line = (not self.multi_class)
        return df, tgt_name

    def process_sparse(self):
        '''处理离散变量
        '''
        df_cnt = self.df_del.groupby(self.fea)[[self.tgt_name]].count()

        # 同时处理二分类和多分类
        df_plt = self.df_del.groupby([self.fea, self.tgt_name])[self.tgt_name].count()
        df_plt = (df_plt / df_plt.groupby(self.fea).sum()).unstack()  # 换算成比例
        # 对于二分类
        if (not self.multi_class) and (len(df_plt.columns)>1):
            df_plt = df_plt[[df_plt.columns[1]]].sort_values(df_plt.columns[1])
        # df_plt = df_plt.groupby(fea)[tgt_name].mean().sort_values()  # 二分类
        return df_plt, df_cnt

    def process_dense(self):
        '''处理连续变量
        '''
        __fea = '__' + self.fea
        # 同时处理二分类和多分类
        df_plt = self.df.groupby([__fea, self.tgt_name])[self.tgt_name].count()
        df_plt = (df_plt / df_plt.groupby(__fea).sum()).unstack()  # 换算成比例
        df_plt = df_plt if self.multi_class else df_plt[[df_plt.columns[1]]]
        # df_plt = df.groupby(__fea)[tgt_name].mean()  # 二分类
        df_cnt = self.df.groupby(__fea)[self.tgt_name].count()
        return df_plt, df_cnt
    
    def plot_left(self):
        # 绘制客户占比折线图
        for col in self.df_plt.columns:
            self.ax1.plot(self.xticks, self.df_plt[col].values)
        if self.multi_class:
            self.ax1.legend(self.get_left_legend())

    def plot_right(self):
        # 绘制客户量bar图
        if self.fea in self.dense_list:
            yticks = self.df_cnt.values
        else:
            yticks = [self.df_cnt.loc[col, self.tgt_name] for col in self.df_plt.index]

        # 对yticks做后处理
        if self.bar_yticks_func is not None:
            yticks = [self.bar_yticks_func(ytick) for ytick in yticks]
        self.ax2.bar(self.xticks, yticks, alpha=self.alpha, facecolor=self.facecolor)
        
        # 绘制bar数量
        if self.plot_text in {'right', 'both'}:
            for x, y in zip(range(len(self.xticks)), yticks):
                self.ax2.text(x, y, y, ha='center', va='bottom')
