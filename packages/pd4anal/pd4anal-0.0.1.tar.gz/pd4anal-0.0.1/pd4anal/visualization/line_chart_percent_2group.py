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


class LineChartPercent2Group(LineChartPercentBase):
    def __init__(self, name='line_chart_percent_2group', plot_pos_ratio=True, **kwargs):
        '''LineChartPercent的兄弟版本，折线图和均值线默认表示pos占比，区别是pos和neg是双柱，且可选择表示“目标客户”和"非目标客户"占比
        
        param plot_pos_ratio: bool, True表示绘制pos的占比，False表示绘制pos/neg的比例
        '''
        super().__init__(**kwargs)
        self.name = name
        self.plot_pos_ratio = plot_pos_ratio
        if plot_pos_ratio:
            print(f'[INFO] Arg `plot_pos_ratio`={plot_pos_ratio} and linechart represents pos/total ratio')
        else:
            print(f'[INFO] Arg `plot_pos_ratio`={plot_pos_ratio} and linechart represents pos/neg ratio')

    def process_sparse(self):
        '''处理离散变量
        '''
        df_cnt = self.df_del.groupby([self.fea, self.tgt_name])[self.tgt_name].count().to_frame('count').reset_index()
        # 处理二分类
        df_plt = self.df_del.groupby([self.fea, self.tgt_name])[self.tgt_name].count().unstack()
        if self.plot_pos_ratio:
            df_plt = (df_plt[df_plt.columns[1]] / (df_plt.sum(axis=1) + 1e-5))  # pos占比
        else:
            df_plt = (df_plt[df_plt.columns[1]] / (df_plt[df_plt.columns[0]] + 1e-5))  # pos/neg
        # 递增排序
        df_plt.fillna(0, inplace=True)
        df_plt = df_plt.sort_values()

        return df_plt, df_cnt

    def process_dense(self):
        '''处理连续变量
        '''
        # 二分类
        __fea = '__' + self.fea
        df_plt = self.df.groupby([__fea, self.tgt_name])[self.tgt_name].count().unstack()
        if self.plot_pos_ratio:
            df_plt = (df_plt[df_plt.columns[1]] / (df_plt.sum(axis=1) + 1e-5))  # pos占比
        else:
            df_plt = (df_plt[df_plt.columns[1]] / (df_plt[df_plt.columns[0]] + 1e-5))  # pos/neg
        df_cnt = self.df.groupby([__fea, self.tgt_name])[self.tgt_name].count().to_frame('count').reset_index()
        return df_plt, df_cnt
    
    def plot_left(self):
        # 绘制客户占比折线图
        self.ax1.plot(self.xticks, self.df_plt.values)
        if self.plot_text in {'left', 'both', True}:
            for x, y in zip(range(len(self.xticks)), self.df_plt.values):
                self.ax1.text(x, y, f'{self.set_precision(y)}', ha='center', va='bottom')

    def plot_right(self):
        x = '__'+self.fea if self.fea in self.dense_list else self.fea
        sns.barplot(data=self.df_cnt, x=x, y='count', hue=self.tgt_name, alpha=self.alpha, ax=self.ax2, order=self.df_plt.index)
        self.ax2.set_xticklabels(labels=self.xticks, rotation=self.rotation, horizontalalignment=self.horizontalalignment)
        if self.remove_legend:
            self.ax2.legend_.remove()
        else:
            self.ax2.legend(loc='upper right')
        # 绘制bar数量
        if self.plot_text in {'right', 'both', True}:
            yticks = self.df_cnt.pivot(index=x, columns=self.tgt_name, values='count').loc[self.df_plt.index]
            # for x, y in zip(range(len(self.xticks)), yticks.values):
            #     self.ax2.text(x, max(y), f'{y[0]:.0f}\n{y[1]:.0f}', ha='center', va='bottom', color='red', alpha=0.7)
            for x, y in zip(range(len(self.xticks)), yticks.values):
                y1, y2 = y[0], y[1]
                y_text = f'{y1:.0f}\n'
                self.ax2.text(x, max(y1, y2), y_text, ha='center', va='bottom', color=sns.color_palette()[0], alpha=1)
                y_text = f'\n{y2:.0f}'
                self.ax2.text(x, max(y1, y2), y_text, ha='center', va='bottom', color=sns.color_palette()[1], alpha=1)

    def plot_axhline(self):
        # 绘制平均客户倍数
        if (self.plot_pos_ratio is False) and (self.avg_line is True):
            tmp = self.df.groupby(self.tgt_name)[self.tgt_name].count()
            if len(tmp) >= 2:
                self.ax1.axhline(y=tmp[tmp.index[1]]/tmp[tmp.index[0]], ls='--', lw=1, color='gray')
            return
        super().plot_axhline()
