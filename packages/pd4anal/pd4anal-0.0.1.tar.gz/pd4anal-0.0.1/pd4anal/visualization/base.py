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
import re
import copy
from pd4anal.utils import is_dtype_numberic

class VisualBase(object):
    def __init__(self, save_path=None, sparse_list=[], dense_list=[], feature_importance={}, bin_count=10, bins=None, bin_cutmode='qcut', bin_replace_inf=True,
                 ncols=4, figsize=(20,20), subplot_size=(5,5), title='', title_max_len=15, use_definition=False, use_enum=False, plot_text=False, bar_yticks_func=None, 
                 dense_round=1, eps=1e-6, min_count=0.01, rotation=45, horizontalalignment='center', subtitle_postfix='', remove_legend=False, **kwargs):
        '''VisualBase
        args:
            sparse_list: list, 离散变量名list
            dense_list:  list, 连续变量名list
            use_definition: bool, 使用schema_center的中文指标名来画图
            ncols: int, 绘图列数
            figsize: tuple, 图片的大小
            subplot_size: tuple, subplot中一个窗口图片的大小，若设置了，则figsize无效
            title: str, 总图的title
            title_max_len: int, 子图的title最大长度
            rotation: int, set_xticklabels中旋转的角度，默认为45
            horizontalalignment: str, set_xticklabels中横向对齐，默认为center，当label名称较长时候设置为right更容易看
            dense_round: int, 绘图时候dense变量需要保留的精度，默认精度为1，如0.023123为0.023, <0表示不采用
            use_enum: bool, 离散变量（枚举型）使用字典替换
            min_count: float, 离散变量指定每个离散值(箱体)最小的占比, >1时候表示数量
            bin_count: int, 连续变量qcut的分箱数量
            bins: dict, 连续变量cut的参数, 用于指定切分的边界，如{'aum':[-np.inf,0,10000,50000,200000,500000,np.inf]}, 默认为None
            bin_cutmode: str, 'qcut'表示按照比例切分，'cut'表示按照区间平均切分，优先级低于bins参数
            bin_replace_inf: bool, 是否替换-np.inf为min，np.inf为max，以提供更多的信息
            plot_text: bool, bar图是否打印数量，默认为False
            bar_yticks_func: function, 对ytick做后处理的函数，默认为None
            subtitle_postfix: subtitle后缀
            remove_legend: 是否去除legend
        '''
        self.save_path = save_path
        self.sparse_list = sparse_list
        self.dense_list = dense_list
        self.bin_count = bin_count
        self.bins = copy.deepcopy(bins)
        self.ncols = ncols
        self.figsize = figsize
        self.subplot_size = subplot_size
        self.title = title
        self.title_max_len = title_max_len
        self.use_definition = use_definition
        self.use_enum = use_enum
        self.feature_importance = feature_importance
        self.min_count = min_count
        self.rotation = rotation
        self.horizontalalignment = horizontalalignment
        assert plot_text in {'left', 'right', 'both', False, True}
        self.plot_text = plot_text
        self.bar_yticks_func = bar_yticks_func
        self.dense_round = dense_round
        self.subtitle_postfix = subtitle_postfix
        self.bin_cutmode = bin_cutmode
        self.bin_replace_inf = bin_replace_inf
        self.eps = eps
        self.remove_legend = remove_legend
        if self.min_count > 0:
            tmp = 'count' if self.min_count >= 1 else 'ratio'
            print(f"[INFO] Arg `min_count`={self.min_count} and sparse bins will be ignored when bin {tmp} under {self.min_count}")

    def trans_df(self, df_X, df_y):
        '''df的修改和tgt_name的获取
        '''
        df = df_X.copy()
        if df_y is not None:
            tgt_name = df_y.name
            df[tgt_name] = df_y
            df[tgt_name] = df[tgt_name].astype(float)
            assert df[tgt_name].nunique() >= 2, f'{tgt_name} class num not >=2'
        else:
            tgt_name = None
        return df, tgt_name

    def get_dense_sparse_list(self, tracker, df, skip_feats=[]):
        '''修改dense_list和sparse_list，并生成fea_list
        '''
        if isinstance(skip_feats, str):
            skip_feats = [skip_feats]

        self.sparse_list += [i for i in tracker.get('sparse_list', []) if i not in self.sparse_list]
        self.dense_list += [i for i in tracker.get('dense_list', []) if i not in self.dense_list]

        if tracker.get('feature_importance', None):
            # fea_importance: 因子重要度，可以是iv，模型出的因子重要度等
            # 根据feature_importance排序
            self.feature_importance.update(tracker['feature_importance'])
            self.feature_importance = [(k, v) for k, v in tracker['feature_importance'].items()]
            self.feature_importance = OrderedDict(sorted(self.feature_importance, key=lambda x: x[1], reverse=True))
            fea_list = []
            for key in self.feature_importance.keys():
                if key in self.sparse_list + self.dense_list:
                    fea_list.append(key)
            for key in self.sparse_list + self.dense_list:
                if key not in fea_list:
                    fea_list.append(key)
        elif len(self.sparse_list) + len(self.dense_list) > 0:
            fea_list = [col for col in df.columns if col in self.sparse_list + self.dense_list]
        else:
            fea_list = [col for col in df.columns if col not in skip_feats]
            self.dense_list = [col for col in fea_list if is_dtype_numberic(df[col])]
            self.sparse_list = [col for col in fea_list if col not in self.dense_list]
        return fea_list

    def get_axes(self, subplot_nums):
        '''根据行列个数生成axes
        '''
        nrows = math.ceil(subplot_nums / self.ncols)
        if nrows <= 1:
            self.ncols = subplot_nums
        if self.subplot_size is not None:
            self.figsize = (self.subplot_size[0]*self.ncols, self.subplot_size[1]*nrows)
            print(f'[INFO] Args `figsize` has been set to {self.figsize} according to args `subplot_size`')
        fig, axes = plt.subplots(nrows=nrows, ncols=self.ncols, sharey=False, squeeze=False, figsize=self.figsize)
        return fig, axes

    def set_precision(self, num):
        '''设置数字的精度
        '''
        if np.isinf(num):
            return num
        if abs(num) >= 10:
            return int(round(num))

        precision = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
        for len_, prec in enumerate(precision):
            if abs(num) >= prec:
                return round(num, len_+self.dense_round)
        return num

    def set_xticks(self, fea, index_, sr, ax):
        '''使用枚举值替换xticks
        fea: 特征名称
        index_: df的index
        sr: 该列特征
        ax: 绘图用的ax
        '''
        # 连续变量要控制左右边界的输出格式
        if (self.dense_round > 0) and (fea in self.dense_list):
            new_index = []
            for bound in index_:
                _left, _right =  self.set_precision(bound.left), self.set_precision(bound.right)
                if _left < _right:
                    # 防止round后left==right
                    new_index.append(f'({_left}, {_right}]')
                else:
                    new_index.append(f'({bound.left}, {bound.right}]')
            # 最左侧边界的处理: '(' -> '['
            if float(new_index[0][1:].split(',')[0]) in sr:
                new_index[0] = '[' + new_index[0][1:]
            self.xticks = new_index
        else:
            self.xticks = list(index_.map(str))

        if self.use_enum and schemacenter[fea] and schemacenter[fea].enum:
            # 尝试把float型的字符串"1.0"，转为int型字符串"1"
            xticks = []
            for i in self.xticks:
                if re.search('^[0-9]+\.0$', i) and int(float(i)) == float(i):
                    i = str(int(float(i)))
                xticks.append(schemacenter[fea].enum.get(i, i))
            self.xticks = xticks
        ax.set_xticklabels(labels=self.xticks, rotation=self.rotation, horizontalalignment=self.horizontalalignment)
        return self.xticks

    def sub_title(self, fea):
        '''使用schema_center的中文指标名来写标题
        '''
        if self.use_definition and schemacenter[fea]:
            plot_fea = schemacenter[fea].definition
        else:
            plot_fea = fea

        if self.feature_importance.get(fea, None):
            sub_title = f"{plot_fea}-{self.set_precision(self.feature_importance[fea])}"
        else:
            sub_title = plot_fea
        
        if fea in self.subtitle_postfix:
            sub_title += '-' + str(self.subtitle_postfix[fea])
        
        # 最大长度要添加换行
        if len(sub_title) > self.title_max_len:
            sub_title_list = [sub_title[i:i+self.title_max_len] for i in range(0, len(sub_title), self.title_max_len)]
            sub_title = '\n'.join(sub_title_list)

        return sub_title

    def save_figure(self):
        '''保存图片
        '''
        if self.title != '':
            plt.suptitle(self.title)
        plt.tight_layout()

        if self.save_path:
            # 保存文件
            save_dir = '/'.join(self.save_path.split('/')[:-1])
            save_file = self.save_path.split('/')[-1].split('.')[0] + '.jpg'
            os.makedirs(save_dir, exist_ok=True)
            plt.savefig(os.path.join(save_dir, save_file), dpi=100, bbox_inches='tight')
        plt.show()

    def replace_inf(self, df, fea):
        '''替换bins参数中的-np.inf和np.inf，当且仅当self.bin_replace_inf=True的时候生效
        '''
        if not self.bin_replace_inf:
            return
        
        for i, item in enumerate(self.bins[fea]):
            notna_df_fea = df[fea].loc[~df[fea].isna()]
            if item == -np.inf:
                self.bins[fea][i] = min(min(notna_df_fea), self.bins[fea][1])
            elif item == np.inf:
                self.bins[fea][i] = max(max(notna_df_fea), self.bins[fea][-2])


class LineChartPercentBase(VisualBase):
    def __init__(self, alpha=0.2, facecolor='gray', left_ylim=None, right_ylim=None,  avg_line=True, **kwargs):
        '''LineChartPercentBase
        args:
            alpha: float, 柱状图的透明度，默认为0.2
            facecolor: str, 柱状图的颜色，默认为灰色gray
            left_ylim: list, 左轴范围
            right_ylim: list, 右轴范围
            avg_line: 绘制均值线
        '''
        super().__init__(**kwargs)   
        self.alpha = alpha
        self.facecolor = facecolor
        self.left_ylim = left_ylim
        self.right_ylim = right_ylim
        self.avg_line = avg_line
    
    def fit(self, df_X, df_y, **tracker):
        df, tgt_name = self.trans_df(df_X, df_y)  # 合并df
        self.df = df
        self.tgt_name = tgt_name
        self.tgt_cols = [tgt_name, self.hue] if hasattr(self, 'hue') else [tgt_name]

        # 修改dense_list和sparse_list，并生成fea_list
        fea_list = self.get_dense_sparse_list(tracker, df, skip_feats=self.tgt_cols)
        # 获取绘图用的fig和axes
        fig, axes = self.get_axes(len(fea_list))
        for i, fea in enumerate(fea_list):
            try:
                self.fea = fea
                self.ax1 = axes[int(i/self.ncols),i%self.ncols]  # 左轴

                if fea in self.tgt_cols:
                    continue

                # ================预处理================    
                # 离散变量
                elif fea in self.sparse_list:
                    df_cnt = df.groupby(fea)[[tgt_name]].count()
                    # 最低数量: <1表示比例，>1表示数量
                    min_count = self.min_count*(~df[fea].isna()).sum() if self.min_count < 1.0 else self.min_count
                    df_cnt = df_cnt[df_cnt[tgt_name] > min_count]

                    if df_cnt.shape[0] == 0:
                        warnings.warn(f'fea {fea} valid count is not enough')
                        continue

                    # try catch的目的是有时候merge，两边的fea的类型对不上
                    try:
                        # df_cnt作用就是筛选数据量过小的分箱
                        self.df_del = pd.merge(df[[fea]+self.tgt_cols], df_cnt.reset_index()[[fea]], on=fea)
                    except:
                        # merge失败，不进行删减数据
                        warnings.warn(traceback.format_exc())
                        self.df_del = df[[fea]+self.tgt_cols]
                    
                    self.df_plt, self.df_cnt = self.process_sparse()
                    # 按照想要的顺序排序，如资产层级、会员等级等有大小关系的离散指标
                    if (self.bins is not None) and (fea in self.bins):
                        index_sort, index_drop = [], []
                        for i in self.bins[self.fea]:
                            if i in self.df_plt.index:
                                index_sort.append(i)
                            elif i not in self.df[fea].unique():
                                index_drop.append(i)
                        if len(index_sort) == 0:
                            warnings.warn("Arg `bins`= {" + f"'{fea}':{self.bins[self.fea]}" + "}" + f" don't match actual enum {list(self.df_plt.index)}, " + \
                                          f"you may use df['{fea}'].unique() to check first")
                        else:
                            self.df_plt = self.df_plt.loc[index_sort]
                        if len(index_drop) > 0:
                            print(f"[Warning] Arg `bins`'s {fea} receive upexpected values {index_drop}")

                # 连续变量
                elif fea in self.dense_list:
                    __fea = '__' + fea
                    # 自定义切分，适用于有业务含义时候，如aum以1万，5万，20万等作为分割点
                    if (self.bins is not None) and (fea in self.bins):
                        # 如果有指定bins则使用cut, 此时格式为[-np.inf, 0, 10000, 10000, np.inf]
                        assert len(self.bins[fea]) > 1, f'Args `bins` {fea} only support >1 split points'
                        self.replace_inf(df, fea)
                        df[__fea] = pd.cut(df[fea], self.bins[fea], duplicates='drop', retbins=True, include_lowest=True)[0]
                    # 等距切分
                    elif self.bin_cutmode == 'cut':
                        # 这里默认的cut会导致边界没有含义，因此这里是自己切分
                        min_, max_ = df[fea].min(), df[fea].max()
                        start, bins = min_, [min_-self.eps]
                        while True:
                            start = start + (max_-min_)/self.bin_count
                            if start >= max_-self.eps:
                                break
                            bins.append(start)
                        bins.append(max_+self.eps)
                        df[__fea] = pd.cut(df[fea], bins, duplicates='drop', retbins=True, include_lowest=True)[0]
                    # 等量切分
                    elif self.bin_cutmode == 'qcut':
                        # df[__fea] = pd.qcut(df[fea], q=bin_count, duplicates='drop', labels=False)
                        df[__fea] = pd.qcut(df[fea], q=self.bin_count, duplicates='drop', retbins=True)[0]
                    else:
                        raise ValueError('Args `bins` and `bin_cunmode` is illegal')
                    self.df_plt, self.df_cnt = self.process_dense()

                # ================绘图区================
                # 设置xticks
                self.set_xticks(self.fea, self.df_plt.index, df[fea], self.ax1)

                # 绘制做轴
                self.plot_left()

                # 绘制右轴
                self.ax2 = self.ax1.twinx() if tgt_name is not None else ax1
                self.plot_right()

                # 绘制子图标题
                self.ax1.set_title(self.sub_title(self.fea))

                # 设置ylim, plot_text等
                self.set_plot_format()
            except:
                print(f'[ERROR] Fea={fea} visualization error...')
                print(traceback.format_exc())
        self.save_figure()
        return df_X, df_y, tracker

    def process_sparse(self):
        '''处理离散变量
        '''
        raise NotImplementedError

    def process_dense(self):
        '''处理连续变量
        '''
        raise NotImplementedError
    
    def plot_left(self):
        raise NotImplementedError

    def plot_right(self):
        raise NotImplementedError

    def set_plot_format(self):
        def get_ylim(raw_ylim, set_ylim):
            # 为了防止超出预设的ylim， 所以这里用每张图给各自的ylim比较，取较大的区间
            return [min(raw_ylim[0], set_ylim[0]), max(raw_ylim[1], set_ylim[1])]

        # 设置左轴范围
        if self.left_ylim is not None:
            left_ylim = get_ylim(self.ax1.get_ylim(), self.left_ylim)
            self.ax1.set_ylim(left_ylim)

        # 设置右轴范围
        if self.right_ylim is not None:
            right_ylim = get_ylim(self.ax2.get_ylim(), self.right_ylim)
            self.ax2.set_ylim(right_ylim)
            self.ax2.set_ylabel(None)

        # 绘制均值线
        self.plot_axhline()

    def get_left_legend(self):
        try:
            legend = list(self.df_plt.columns.map(int).map(str))
        except:
            legend = list(self.df_plt.columns.map(str))
        if self.use_enum and schemacenter[self.tgt_name] and schemacenter[self.tgt_name].enum:
            legend = [schemacenter[self.tgt_name].enum.get(i, i) for i in legend]
        return legend

    def plot_axhline(self):
        # 绘制指定值
        if (self.avg_line is not True)  and isinstance(self.avg_line, (int, float)):
            self.ax1.axhline(y=self.avg_line, ls='--', lw=1, color='gray')
        # 绘制目标客户平均占比
        elif self.avg_line is True:
            self.ax1.axhline(y=self.df[self.tgt_name].mean(), ls='--', lw=1, color='gray')
