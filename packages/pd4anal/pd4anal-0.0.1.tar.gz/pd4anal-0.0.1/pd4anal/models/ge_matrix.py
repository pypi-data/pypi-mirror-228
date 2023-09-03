import os
import pandas as pd
import seaborn as sns
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class GeMatrix(object):
    def __init__(self, index, columns, save_path='', index_bins=None, columns_bins=None, sparse_fea_sort={}, dense_bin_count=10, 
                 dense_cut_mode='cut', cal_density=False, figsize=(8,8), choice='default', pipeline_return=False, **kwargs):
        '''依据传入的index和columns来绘制九宫格图
        index: 行名
        columns: 列名
        save_path: 图保存的目录
        index_bins: 需要手动指定index的切分边界，默认为None
        columns_bins: 需要手动指定index的切分边界，默认为None
        sparse_fea_sort: {fea: [fea_list]}, 仅对离散变量配置，用于指定离散变量的排列顺序
        dense_bin_count: 连续值需要划分的箱体数量，若指定了index_bins/column_bins，则不生效
        dense_cut_mode: 连续变量是使用cut还是qcut
        cal_density: 是否计算格子的密度，即绘制出来是比例
        figsize: 绘制的figure尺寸
        choice: default, add_margin_subplots(subplots方式添加边缘分布), add_margin_gridsepc(gridsepc方式添加边缘分布)
        '''
        self.index = index
        self.columns = columns
        self.index_bins = index_bins
        self.columns_bins = columns_bins
        self.sparse_fea_sort = sparse_fea_sort
        self.dense_bin_count = dense_bin_count
        self.dense_cut_mode = dense_cut_mode
        self.cal_density = cal_density
        self.choice = choice
        self.save_path = save_path
        self.pipeline_return = pipeline_return
        self.figsize = figsize
        self.ratio = kwargs.get('ratio', 5)  # 用于gridsepc模式

        self.group_data = None  # 分组统计的个数信息
        self.pivot_data = None  # pivot用于绘图的信息

    def fit(self, df_X, y=None, **tracker):
        df_base = df_X.copy()
        #     sns.set_theme(style="darkgrid")
        for fea, fea_bins in [[self.index, self.index_bins], [self.columns, self.columns_bins]]:
            # 离散变量不需要切分
            if df_base[fea].dtype == 'O' or fea in self.sparse_fea_sort.keys():
                continue
            elif self.dense_cut_mode == 'qcut':
                df_base[fea] = pd.qcut(df_base[fea], q=self.dense_bin_count, duplicates='drop', retbins=True)[0]
            # 等距切分
            elif fea_bins is None:
                df_base[fea] = pd.cut(df_base[fea], self.dense_bin_count)
            # 按照指定的bins来切分
            else:
                df_base[fea] = pd.cut(df_base[fea], fea_bins)

        data = df_base.groupby([self.index, self.columns]).size().reset_index()
        data = data.rename(columns={0: 'count'})

        xdf = data.pivot(index=self.index, columns=self.columns, values='count')
        
        # 排序
        if self.index in self.sparse_fea_sort:
            xdf = xdf.loc[self.sparse_fea_sort[self.index]]
        else:
            xdf.sort_values(self.index, ascending=False, inplace=True)  # 默认降序，图形y轴升序
        if self.columns in self.sparse_fea_sort:
            xdf = xdf[self.sparse_fea_sort[self.columns]]
        
        # 计算格子的密度
        if self.cal_density:
            for i in xdf.index:
                for j in xdf.columns:
                    xdf.loc[i, j] = xdf.loc[i, j] / ((i.right-i.left) * (j.right - j.left))
        
        # ======================绘图区
        if self.choice == 'default':
            # =======================两个特征的下宫格分布图
            plt.figure(figsize=self.figsize)
            sns.heatmap(xdf, linewidths =0.01, cmap='Blues', xticklabels=xdf.columns, yticklabels=xdf.index)
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
            plt.xlabel(self.columns)
            plt.ylabel(self.index)

        elif self.choice == 'add_margin_subplots':
            # =======================subplots方式添加两个特征的边缘分布（存在右上角的格子）
            fig,ax = plt.subplots(nrows=2,ncols=2,sharey=False,squeeze=False, figsize=self.figsize)
            # x边缘分布
            plt.subplot(2, 2, 1)
            df_tmp = xdf.sum(axis=0)
            plt.bar(df_tmp.index, df_tmp.values, color='gray')
            # 联合分布
            plt.subplot(2, 2, 3)
            sns.heatmap(xdf, linewidths =0.01,cmap='Blues')
            # y边缘分布
            plt.subplot(2, 2, 4)
            df_tmp = xdf.sum(axis=1)
            plt.barh(df_tmp.index.map(str), df_tmp.values, color='gray')
            
        elif self.choice == 'add_margin_gridsepc':
            # =======================gridsepc方式添加两个特征的边缘分布（存不在右上角的格子）
            f = plt.figure(figsize=self.figsize)
            gs = plt.GridSpec(self.ratio + 1, self.ratio + 1)

            ax_joint = f.add_subplot(gs[1:, :-1])
            ax_marg_x = f.add_subplot(gs[0, :-1], sharex=ax_joint)
            ax_marg_y = f.add_subplot(gs[1:, -1], sharey=ax_joint)

            fig = f
            ax_joint = ax_joint
            ax_marg_x = ax_marg_x
            ax_marg_y = ax_marg_y

            # Turn off tick visibility for the measure axis on the marginal plots
            plt.setp(ax_marg_x.get_xticklabels(), visible=False)
            plt.setp(ax_marg_y.get_yticklabels(), visible=False)
            plt.setp(ax_marg_x.get_xticklabels(minor=True), visible=False)
            plt.setp(ax_marg_y.get_yticklabels(minor=True), visible=False)

            # Turn off the ticks on the density axis for the marginal plots
            plt.setp(ax_marg_x.yaxis.get_majorticklines(), visible=False)
            plt.setp(ax_marg_x.yaxis.get_minorticklines(), visible=False)
            plt.setp(ax_marg_y.xaxis.get_majorticklines(), visible=False)
            plt.setp(ax_marg_y.xaxis.get_minorticklines(), visible=False)
            plt.setp(ax_marg_x.get_yticklabels(), visible=False)
            plt.setp(ax_marg_y.get_xticklabels(), visible=False)
            plt.setp(ax_marg_x.get_yticklabels(minor=True), visible=False)
            plt.setp(ax_marg_y.get_xticklabels(minor=True), visible=False)
            ax_marg_x.yaxis.grid(False)
            ax_marg_y.xaxis.grid(False)

            # 联合分布
            plt.sca(ax_joint)
            sns.heatmap(xdf, linewidths =0.01,cmap='Blues')

            # x边缘分布
            plt.sca(ax_marg_x)
            df_tmp = xdf.sum(axis=0)
            ax_marg_x.bar(df_tmp.index, df_tmp.values, color='gray', align='edge')

            # y边缘分布
            plt.sca(ax_marg_y)
            df_tmp = xdf.sum(axis=1)
            ax_marg_y.barh(df_tmp.index.map(str), df_tmp.values, color='gray', align='edge')
        
        if self.save_path:
            # 保存文件
            save_dir = '/'.join(self.save_path.split('/')[:-1])
            save_file = self.save_path.split('/')[-1].split('.')[0] + '.jpg'
            os.makedirs(save_dir, exist_ok=True)
            plt.savefig(os.path.join(save_dir, save_file), dpi=100, bbox_inches='tight')
        self.group_data = data
        self.pivot_data = xdf
        
        if self.pipeline_return:
            df_y = tracker.pop('df_y') if 'df_y' in tracker else None
            return df_X, df_y, tracker
        else:
            return xdf


class GeMatrixPie(object):
    def __init__(self, index, columns, target, save_path='', index_bins=None, columns_bins=None, sparse_fea_sort={}, dense_bin_count=10, 
                 dense_cut_mode='cut', cal_density=False, grid_size=5, fig_type='pie', colours=None, pipeline_return=False, **kwargs):
        '''依据传入的index和columns来绘制九宫格图, 含target列
        index: 行名
        columns: 列名
        target: 列名，用户在每个格子绘制子图用到
        index_bins: 需要手动指定index的切分边界，默认为None
        columns_bins: 需要手动指定index的切分边界，默认为None
        sparse_fea_sort: {fea: [fea_list]}, 仅对离散变量生效，用于指定离散变量的排列顺序
        dense_bin_count: 连续值需要划分的箱体数量，若指定了index_bins/column_bins，则不生效
        dense_cut_mode: 连续变量是使用cut还是qcut
        cal_density: 是否计算格子的密度，即绘制出来是比例
        grid_size：每个格子的大小
        fig_type：每个格子的图类型
        colours: label对应的颜色字典
        '''
        self.index = index
        self.columns = columns
        self.target = target
        self.save_path = save_path
        self.index_bins = index_bins
        self.columns_bins = columns_bins
        self.sparse_fea_sort = sparse_fea_sort
        self.dense_bin_count = dense_bin_count
        self.dense_cut_mode = dense_cut_mode
        self.cal_density = cal_density
        self.grid_size = grid_size
        self.fig_type = fig_type
        self.colours = colours
        self.pipeline_return = pipeline_return

        self.group_data = None  # 分组统计的个数信息
        self.pivot_data = None  # pivot用于绘图的信息

    def fit(self, df_X, **tracker):
        color_list = []
        df_base = copy.deepcopy(df_X)
        df_base[self.index+'_cp'] = df_base[self.index]
        df_base[self.columns+'_cp'] = df_base[self.columns]
        
        for fea, fea_bins in [[self.index, self.index_bins], [self.columns, self.columns_bins]]:
            # 离散变量不需要切分
            if df_base[fea].dtype == 'O' or fea in self.sparse_fea_sort.keys():
                continue
            elif self.dense_cut_mode == 'qcut':
                df_base[fea] = pd.qcut(df_base[fea], q=self.dense_bin_count, duplicates='drop', retbins=True)[0]
            # 等距切分
            elif fea_bins is None:
                df_base[fea] = pd.cut(df_base[fea], self.dense_bin_count)
            # 按照指定的bins来切分
            else:
                df_base[fea] = pd.cut(df_base[fea], fea_bins)

        data = df_base.groupby([self.index, self.columns]).size().reset_index()
        data = data.rename(columns={0: 'count'})

        xdf = data.pivot(index=self.index, columns=self.columns, values='count')
        
        # 排序
        if self.index in self.sparse_fea_sort:
            xdf = xdf.loc[self.sparse_fea_sort[self.index]]
        else:
            xdf.sort_values(self.index, ascending=False, inplace=True)  # 默认降序，图形y轴升序
        if self.columns in self.sparse_fea_sort:
            xdf = xdf[self.sparse_fea_sort[self.columns]]
        
        # 计算格子的密度
        if self.cal_density:
            for i in xdf.index:
                for j in xdf.columns:
                    xdf.loc[i, j] = xdf.loc[i, j] / ((i.right-i.left) * (j.right - j.left))
        
        cmap = plt.cm.Blues
        norm = matplotlib.colors.Normalize(vmin=xdf.values.min(), vmax=xdf.values.max())
        # ================================绘图区域================================
        nrows, ncols = xdf.shape
        figsize = ncols * self.grid_size, nrows * self.grid_size
        fig,ax = plt.subplots(nrows=nrows,ncols=ncols,sharey=False,squeeze=False,figsize=figsize)
        for i, ind in enumerate(xdf.index):
            for j, col in enumerate(xdf.columns):
                df_tmp = df_base.loc[(df_base[self.columns]==col) & (df_base[self.index]==ind)]
                plt.subplot(nrows, ncols, i*ncols+j+1)
                face_color = cmap(norm(xdf.values[i, j]))
                # 背景着色
                cur_ax = plt.gca()
                cur_ax.patch.set_facecolor(face_color)
                
                if self.fig_type is None:
                    continue
                elif self.fig_type == 'pie':
                    radius = 0.15+xdf.values[i, j]/xdf.values.max()*0.35
                    _plot_pie(df_tmp, self.index, self.columns, self.target, plt, radius, self.colours)
                    if i == len(xdf.index)-1:
                        plt.xlabel(xdf.columns[j])
                    if j == 0:
                        plt.ylabel(xdf.index[i])
                else:
                    # 两边都是连续型
                    if df_tmp[self.columns+'_cp'].nunique() > 1 and df_tmp[self.index+'_cp'].nunique() > 1:
                        _plot_2d_scatter(df_tmp, self.index, self.columns, self.target, plt)
                    elif df_tmp[self.columns+'_cp'].nunique() * df_tmp[self.index+'_cp'].nunique() > 1:
                        _plot_1d_bar(df_tmp, self.index, self.columns, self.target, plt)           
                
        plt.tight_layout()
        self.group_data = data
        self.pivot_data = xdf

        if self.pipeline_return:
            df_y = tracker.pop('df_y') if 'df_y' in tracker else None
            return df_X, df_y, tracker
        else:
            return 


def _plot_2d_scatter(df_tmp, index, columns, target, plt):
    '''散点图
    '''
    if target is None:
        plt.scatter(df_tmp[columns+'_cp'], df_tmp[index+'_cp'])
    elif isinstance(target, str):
        df_tmp1 = df_tmp.loc[df_tmp[target] == 1]
        plt.scatter(df_tmp1[columns+'_cp'], df_tmp1[index+'_cp'])
    elif isinstance(target, list):
        maker_list = ['o', '*', 's', 'p']
        for k, tgt in enumerate(target):
            df_tmp1 = df_tmp.loc[df_tmp[tgt] == 1]
            plt.scatter(df_tmp1[columns+'_cp'], df_tmp1[index+'_cp'], marker=maker_list[k], alpha=0.5)     

def _plot_1d_bar(df_tmp, index, columns, target, plt, dense_bin_count=10):
    '''条形图：横向，纵向
    '''
    func = plt.bar if df_tmp[columns+'_cp'].nunique() > 1 else plt.barh
    if df_tmp[index+'_cp'].nunique() > 1:
        bin_col = index+'_bin'
        df_tmp[bin_col] = pd.cut(df_tmp[index+'_cp'], dense_bin_count)
    else:
        bin_col = columns+'_bin'
        print(bin_col)
        df_tmp[bin_col] = pd.cut(df_tmp[columns+'_cp'], dense_bin_count)
        
    if target is None:
        df_cnt = df_tmp.groupby(index+'_bin').size()
        func([str(i.left) for i in df_cnt.index], df_cnt.values, color='gray', alpha=0.5)
    elif isinstance(target, str):
        df_cnt = df_tmp.loc[df_tmp[target] == 1].groupby(bin_col).size()
        func([str(i.left) for i in df_cnt.index], df_cnt.values, color='gray', alpha=0.5)
    elif isinstance(target, list):
        for k, tgt in enumerate(target):
            df_cnt = df_tmp.loc[df_tmp[tgt] == 1].groupby(bin_col).size()
            func([str(i.left) for i in df_cnt.index], df_cnt.values, alpha=0.5)

def _plot_pie(df_tmp, index, columns, target, plt, radius=1, colours=None):
    '''扇形图
    '''
    df_cnt = df_tmp.groupby(target).size()
    labels = df_cnt.index.map(str)
    if colours is not None:
        plt.pie(df_cnt, labels=labels, colors=[colours[key] for key in labels], radius=radius, center=(0.5, 0.5), frame=True)
    else:
        plt.pie(df_cnt, labels=labels, radius=radius, center=(0.5, 0.5), frame=True)
    plt.xticks([])
    plt.yticks([])
    
def get_pivot(df_new, index, columns, target, sparse_fea_sort={}):
    '''获取数据分布表
    '''
    data = df_new.groupby([index, columns])[target].sum().reset_index()
    xdf1 = data.pivot(index=index, columns=columns, values=target)

    if index in sparse_fea_sort:
        xdf1 = xdf1.loc[sparse_fea_sort[index]]
    else:
        xdf1.sort_values(index, ascending=False, inplace=True)  # 默认降序，图形y轴升序
    if columns in sparse_fea_sort:
        xdf1 = xdf1[sparse_fea_sort[columns]]
    return xdf1
