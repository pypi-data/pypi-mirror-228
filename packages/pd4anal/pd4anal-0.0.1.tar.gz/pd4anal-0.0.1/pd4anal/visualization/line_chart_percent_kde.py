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


class LineChartPercentKde(LineChartPercentBase):
    def __init__(self, name='line_chart_percent', interpolation_density=False, **kwargs):
        '''LineChartPercent的改良版本，对连续值变量使用kde来绘制密度图，而不是分箱的值，目前还存在问题就是对应的折线图绘制不了
        args:
            interpolation_density: 使用kde密度插值来计算占比
        '''
        super().__init__(**kwargs)
        self.name = name
        self.interpolation_density = interpolation_density


    def adjust_density(self, pos_x, total_x, total_y):
        """依照pos_x作为xtick，通过插值来计算对应的total_y
        """
        start = 0
        total_x_new = []
        total_y_new = []
        for x in pos_x:
            # 在tatal_x轴上中对x进行插值
            for i in range(start, len(total_x)-1):
                x1, y1 = total_x[i], total_y[i]
                x2, y2 = total_x[i+1], total_y[i+1]
                if (x1 <= x <= x2) and (x not in total_x_new):
                    y_new = (x-x1) / (x2-x1) * (y2-y1) + y1
                    total_x_new.append(x)
                    total_y_new.append(y_new)
                    start = i
                    continue
        assert len(total_y_new) == len(pos_x), f'{len(total_y_new)} != {len(pos_x)}'

        return total_y_new

    def trans_df(self, df_X, df_y):
        df, tgt_name = super().trans_df(df_X, df_y)  # 合并df
        assert df[tgt_name].nunique() == 2, f'{tgt_name} class num not equal 2'
        return df, tgt_name

    def process_sparse(self):
        '''处理离散变量
        '''
        df_cnt = self.df_del.groupby(self.fea)[[self.tgt_name]].count()

        # 处理二分类
        df_plt = self.df_del.groupby([self.fea, self.tgt_name])[self.tgt_name].count()
        df_plt = (df_plt / df_plt.groupby(self.fea).sum()).unstack()  # 换算成比例

        if len(df_plt.columns)>1:
            df_plt = df_plt[[df_plt.columns[1]]].sort_values(df_plt.columns[1])

        return df_plt, df_cnt

    def process_dense(self):
        '''处理连续变量
        '''
        __fea = '__' + self.fea
        # 同时处理二分类和多分类
        df_plt = self.df.groupby([__fea, self.tgt_name])[self.tgt_name].count()
        df_plt = (df_plt / df_plt.groupby(__fea).sum()).unstack()  # 换算成比例
        df_plt = df_plt[[df_plt.columns[1]]]
        # df_plt = df.groupby(__fea)[tgt_name].mean()  # 二分类
        df_cnt = self.df.groupby(__fea)[self.tgt_name].count()
        return df_plt, df_cnt
    
    def set_xticks(self, *args, **kwargs):
        if self.fea in self.sparse_list:
            super().set_xticks(*args, **kwargs)

    def plot_left(self):
        # 绘制客户占比折线图

        # 离散变量
        if self.fea in self.sparse_list:
            for col in self.df_plt.columns:
                self.ax1.plot(self.xticks, self.df_plt[col].values)
        # 连续变量插值
        elif self.interpolation_density and (self.fea in self.dense_list):
            # 连续值绘制其kde密度分布图
            total_x, total_y = sns.kdeplot(data=self.df, x=self.fea, cut=0, alpha=0).get_lines()[0].get_data()
            pos_x, pos_y = sns.kdeplot(data=self.df.loc[self.df[self.tgt_name]==1], x=self.fea, cut=0, alpha=0).get_lines()[1].get_data()
            total_y_new = self.adjust_density(pos_x, total_x, total_y)  # 插值计算

            # 计算客户占比
            total_count = len(self.df)
            pos_count = len(self.df.loc[self.df[self.tgt_name]==1])
            plt_y = []
            for x, p_pos, p_total in zip(pos_x, pos_y, total_y_new):
                if p_total*total_count > 0:
                    plt_y.append(p_pos * pos_count / (p_total*total_count))
                else:
                    plt_y.append(0)
            self.ax1.plot(pos_x, plt_y)

        elif self.fea in self.dense_list:
            xticks, yticks = [], []
            for i, id_ in enumerate(self.df_plt.index):
                xticks.append(id_.left)
                yticks.append(self.df_plt.loc[id_].iloc[0])
                if i == len(self.df_plt.index)-1:
                    xticks.append(id_.right)
                    yticks.append(self.df_plt.loc[id_].iloc[0])
            self.ax1.plot(xticks, yticks)

    def plot_right(self):
        if self.fea in self.dense_list:
            sns.kdeplot(data=self.df, x=self.fea, ax=self.ax2, cut=0, fill=True, alpha=self.alpha, color=self.facecolor)
        else:
            self.ax2.bar(self.xticks, [self.df_cnt.loc[col, self.tgt_name] for col in self.df_plt.index], alpha=self.alpha, facecolor=self.facecolor)
