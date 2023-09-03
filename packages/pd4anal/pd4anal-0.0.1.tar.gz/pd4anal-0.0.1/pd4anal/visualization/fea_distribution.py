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
from ..data.schema import schemacenter
from .base import VisualBase
import traceback
from pd4anal.utils import is_dtype_numberic


class FeatureDistribution(VisualBase):
    def __init__(self, name='fea_distribution', method='hist_distribution', pipeline_return=False, 
                 plot_mean=False, plot_median=False, sns_args=None, **kwargs):
        '''特征的分布图, 单变量分布，单变量关于y的分布
        http://seaborn.pydata.org/generated/seaborn.histplot.html
        http://seaborn.pydata.org/generated/seaborn.kdeplot.html
        args:
            method: hist_distribution, kde_distribution, joyplot_distribution, count_distribution, kde_distribution_2d, hist_distribution_2d
            min_count: float, 离散变量指定每个离散值(箱体)最小的占比, >1时候表示数量
            plot_mean: bool, 是否绘制均值
            plot_median: bool, 是否绘制50%分位数

            # hist_distribution: http://seaborn.pydata.org/generated/seaborn.histplot.html
            multiple: 'stack'表示堆叠排布，'dodge'表示并列排布
            stat: 'percent'表示纵轴绘制的占比（百分制），'probability'表示占比（1分制）
        '''
        super().__init__(**kwargs)
        self.method = method
        if 'bins' in kwargs:
            kwargs.pop('bins')
        self.sns_args = dict({'bins': self.bin_count}, **kwargs)
        self.name = name
        self.pipeline_return = pipeline_return
        self.plot_mean = plot_mean
        self.plot_median = plot_median

    def enum_xticks(self, fea, ax):
        # 用枚举值绘制xtick
        xticks = [t.get_text()  for t in ax.get_xticklabels()]
        if self.use_enum and schemacenter[fea] and schemacenter[fea].enum:
            xticks = [schemacenter[fea].enum.get(i, i) for i in xticks]
        ax.set_xticklabels(labels=xticks, rotation=self.rotation, horizontalalignment=self.horizontalalignment)

    def plot_v(self, sr, ax):
        if self.plot_mean:
            v = sr.mean()
            y = (ax.get_ylim()[1]-ax.get_ylim()[0])/3 + ax.get_ylim()[0]
            ax.axvline(x=v, ls='--', lw=1, color='blue')
            ax.text(v, y, f'avg={v:.2f}', ha='left', va='bottom', color='blue')
        if self.plot_median:
            v = sr.median()
            y = (ax.get_ylim()[1]-ax.get_ylim()[0])/3*2 + ax.get_ylim()[0]
            ax.axvline(x=v, ls='--', lw=1, color='red')
            ax.text(v, y, f'50%={v:.2f}', ha='left', va='bottom', color='red')

    def kde_hist_distribution(self, df, tgt_name, fea_list):
        # 获取绘图用的fig和axes
        fig, axes = self.get_axes(len(fea_list))
        for i, fea in enumerate(fea_list):
            try:
                ax = axes[i//self.ncols, i%self.ncols]
                if fea == tgt_name:
                    continue
                
                if not is_dtype_numberic(df[fea]):
                    # 离散变量
                    tmp = df.groupby(fea)[fea].count()
                    tmp.sort_values(inplace=True)
                    df_plt = tmp[tmp > (self.min_count*tmp.sum() if self.min_count<1 else self.min_count)]
                    if True:
                        # 使用countplot绘制柱状图
                        df_cp = df.loc[df[fea].isin(df_plt.index)]
                        sns.countplot(data=df_cp, x=fea, hue=tgt_name, ax=ax, order=df_plt.index, **self.get_kw(sns.countplot))
                        self.enum_xticks(fea, ax)
                    else :
                        # 使用bar绘制柱状图
                        # xticks = list(df_plt.index.map(str))
                        # if use_enum and schemacenter[fea] and schemacenter[fea].enum:
                        #     xticks = [schemacenter[fea].enum.get(i, i) for i in xticks]
                        # ax.bar(xticks, df_plt.values)
                        # ax.set_xticklabels(labels=xticks, rotation=self.rotation, horizontalalignment=self.horizontalalignment)
                        xticks = self.set_xticks(fea, df_plt.index, df[fea], ax)
                        ax.bar(xticks, df_plt.values)

                elif (self.bins is not None) and (fea in self.bins):
                    # 连续变量，按照固定值切分出来
                    __fea = '__' + fea
                    df[__fea] = pd.cut(df[fea], self.bins[fea], duplicates='drop', retbins=True, include_lowest=True)[0]
                    if tgt_name is None:
                        df_cnt = df.groupby(__fea).size()
                        ax.bar(df_cnt.index.map(str), df_cnt.values)
                        for x, y in zip(range(len(df_cnt.index)), df_cnt.values):
                            ax.text(x, y, y, ha='center', va='bottom')
                    else:
                        df_cnt = df.groupby([__fea, tgt_name]).size().unstack()
                        df_cnt.plot.bar(ax=ax)
                    # ax.set_xticklabels(labels=df_cnt.index, rotation=self.rotation, horizontalalignment=self.horizontalalignment)
                    self.set_xticks(fea, df_cnt.index, df[fea], ax)

                elif self.method == 'kde_distribution':
                    # 连续变量kde
                    sns.kdeplot(data=df, x=fea, hue=tgt_name, ax=ax, **self.get_kw(sns.kdeplot))
                    self.plot_v(df[fea], ax)
                elif self.method == 'hist_distribution':
                    # 连续变量hist
                    sns.histplot(data=df, x=fea, hue=tgt_name, ax=ax, **self.get_kw(sns.histplot))
                    self.plot_v(df[fea], ax)
                ax.set_title(self.sub_title(fea))
            except:
                print(f'Fea={fea} visualization error...')
                print(traceback.format_exc())

    def count_distribution(self, df, tgt_name, fea_list):
        # count不能处理数值型的变量
        droplist = []
        fea_list_new = [col for col in fea_list if not is_dtype_numberic(df[col])]
        if len(fea_list_new) != len(fea_list):
            feas = ', '.join([col for col in fea_list if col not in fea_list_new])
            warnings.warn(f'[{feas}] not supported in countplot')
            fea_list = fea_list_new

        # 获取绘图用的fig和axes
        fig, axes = self.get_axes(len(fea_list))
        for i, fea in enumerate(fea_list):
            try:
                if fea == tgt_name:
                    continue
                # 离散变量只能使用countplot绘制柱状图
                sns.countplot(data=df, x=fea, hue=tgt_name, ax=axes[i//self.ncols, i%self.ncols], **self.get_kw(sns.countplot))
            except:
                print(f'Fea={fea} visualization error...')
                print(traceback.format_exc())

    def kde_hist_2ddistributuion(self, df, tgt_name, fea_list):
        # 获取绘图用的fig和axes
        subplot_nums = int(len(fea_list)*(len(fea_list)-1)/2)  # n*(n+1)/2
        fig, axes = self.get_axes(subplot_nums)
        count = 0
        for i, fea_i in enumerate(fea_list[:-1]):
            for j in range(i+1, len(fea_list)):
                try:
                    fea_j = fea_list[j]
                    if (fea_i == tgt_name) or (fea_j == tgt_name):
                        continue
                    if self.method == 'kde_distribution_2d':
                        sns.kdeplot(data=df, x=fea_i, y=fea_j, hue=tgt_name, ax=axes[count//self.ncols, count%self.ncols], **self.get_kw(sns.kdeplot))
                    elif self.method == 'hist_distribution_2d':
                        sns.histplot(data=df, x=fea_i, y=fea_j, hue=tgt_name, ax=axes[count//self.ncols, count%self.ncols], **self.get_kw(sns.histplot))
                    count += 1
                except:
                    print(f'Fea=({fea_i}, {fea_j}) visualization error...')
                    print(traceback.format_exc())
    
    def fit(self, df_X, df_y=None, **tracker):
        # 这里允许没有tgt_name, 即仅绘制分布，而不按照tgt_name作区分
        df, tgt_name = self.trans_df(df_X, df_y)  # 合并df

        # 修改dense_list和sparse_list，并生成fea_list
        fea_list = self.get_dense_sparse_list(tracker, df, skip_feats=[tgt_name])
        
        if self.method in {'kde_distribution', 'hist_distribution'}:
            # 单因素hist/kde图，仅对数值型特征生效, 离散变量调用countplot来实现
            self.kde_hist_distribution(df, tgt_name, fea_list)
        elif self.method == 'count_distribution':
            # 单因素count图，仅对离散型特征生效
            self.count_distribution(df, tgt_name, fea_list)
        elif self.method == 'joyplot_distribution':
            # 单因素峰峦图
            from joypy import joyplot
            column = [i for i in fea_list if i!=tgt_name] if 'column' not in self.sns_args else self.sns_args.pop('column')
            joyplot(df, column=column, by=tgt_name, figsize=self.figsize, **self.get_kw(joyplot))
        elif self.method in {'kde_distribution_2d', 'hist_distribution_2d'}:
            # 双因素
            self.kde_hist_2ddistributuion(df, tgt_name, fea_list)

        self.save_figure()
        
        if self.pipeline_return:
            df_y = tracker.pop('df_y') if 'df_y' in tracker else None
            return df_X, df_y, tracker
        else:
            return 

    def get_kw(self, f):
        from inspect import signature
        sig = signature(f)
        sns_args = {}
        for k, v in self.sns_args.items():
            if k in sig.parameters.keys():
                sns_args[k] = v
        return sns_args
        
