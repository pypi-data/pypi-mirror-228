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
from pd4anal.utils import is_dtype_numberic


class HeatMapPercent(object):
    def __init__(self, save_path=None, name='heat_map_percent', sparse_list=[], dense_list=[], bin_count=10, ncols=5, 
                 title='', min_r=0.1, min_count=10, topk=10, size=5, dense_fill=False, cmap_type='p', fmt='.0f', **kwargs):
        '''根据传入的df的tgt_name，绘制依据双变量的分布图，Z轴为tgt_name中正例占比
        args:
            df_raw: 原始数据
            tgt_name: 目标列
            fea_importance: 因子重要度，可以是iv，模型出的因子重要度等
            bin_count: qcut的分箱数量
            ncols: 绘图列数
            title: 总图的title
            dense_fill: 是否填充连续
            cmap_type: p表示绘制浓度图，count表示绘制y=1的数量热力图
        ''' 
        super().__init__()
        self.save_path = save_path
        self.name = name
        self.sparse_list = sparse_list
        self.dense_list = dense_list
        self.bin_count = bin_count
        self.ncols = ncols
        self.title = title
        self.min_r = min_r
        self.min_count = min_count
        self.topk = topk
        self.size = size
        self.dense_fill = dense_fill
        self.cmap_type = cmap_type
        self.fmt = fmt

    def fit(self, df_X, df_y, **tracker):
        df = df_X.copy()
        tgt_name = df_y.name
        df[tgt_name] = df_y
        
        self.sparse_list += [i for i in tracker.get('sparse_list', []) if i not in self.sparse_list]
        self.dense_list += [i for i in tracker.get('dense_list', []) if i not in self.dense_list]

        if tracker.get('feature_importance', None):
            # 根据feature_importance排序
            feature_importance = [(k, v) for k, v in tracker['feature_importance'].items()]
            feature_importance = OrderedDict(sorted(feature_importance, key=lambda x: x[1], reverse=True))
            fea_list = []
            for key in feature_importance.keys():
                if key in self.sparse_list + self.dense_list:
                    fea_list.append(key)
            # for key in self.sparse_list + self.dense_list:
            #     if key not in fea_list:
            #         fea_list.append(key)
        elif len(self.sparse_list) + len(self.dense_list) > 0:
            fea_list = self.sparse_list + self.dense_list
        else:
            fea_list = [col for col in df_X.columns if col != tgt_name]
            self.dense_list = [col for col in fea_list if is_dtype_numberic(df_X[col])]
            self.sparse_list = [col for col in fea_list if col not in self.dense_list]

        # 交叉特征展示篇幅受限，如果超出topk则做阶段处理
        if len(fea_list) > self.topk:
            print(f'[Warning] Features count is over topk={self.topk} and will be truncated, you may send larger args `topk`')
            fea_list = fea_list[:self.topk]
            self.dense_list = [col for col in fea_list if is_dtype_numberic(df_X[col])]
            self.sparse_list = [col for col in fea_list if col not in self.dense_list]

        nrows, ncols = self.topk+1, self.topk  # 最后一行用来存legend

        # 把连续值分区，离散型去除低频值后填充nan
        dense_fea_map = {}
        for fea in fea_list:
            if fea in self.dense_list:
                bin_map = pd.qcut(df[fea],q=self.bin_count,duplicates='drop', retbins=True)[1]
                df[fea] = pd.qcut(df[fea], q=self.bin_count, duplicates='drop', labels=False) # 直接用分组号
                # 用于打印分组区间信息
                plot_str = ''
                for i, (start,end) in enumerate(zip(bin_map[:-1], bin_map[1:])):
                    plot_str += f'{i} -> ({start:.2f}, {end:.2f}]\n'
                dense_fea_map[fea] = plot_str
            elif fea in self.sparse_list:
                df_cnt = df.groupby(fea, as_index=False).size()
                set_cnt = set(df_cnt.loc[df_cnt['size'] > 0.01*(~df[fea].isna()).sum(), fea].to_list())
                df[fea] = df[fea].apply(lambda x: x if x in set_cnt else np.nan)
        
        # 离散型对nan补全为'nan', 连续型统一补齐
        for fea in self.sparse_list:
            df[fea] = df[fea].fillna('nan')
        
        for fea in self.dense_list:
            if isinstance(self.dense_fill, (int, float)):
                fill_values = self.dense_fill
            elif self.dense_fill is True:
                fill_values = -9999
            else:
                fill_values = -9999
            df[fea] = df[fea].fillna(fill_values)

        figsize = ncols * self.size, nrows * self.size
        fig, ax = plt.subplots(nrows=nrows,ncols=ncols,sharey=False,squeeze=False,figsize=figsize)
        
        for i, index in enumerate(fea_list):
            for j, columns in enumerate(fea_list):
                plt.subplot(nrows, ncols, i*ncols+j+1)
                if index == columns:
                    df_cnt = df.groupby(index)[index].count()
                    plt.bar(df_cnt.index.map(str), df_cnt.values, color='gray')
                    plt.xlabel(index)
                    plt.ylabel(index)
                    plt.xticks(rotation=90)
                else:
                    data = df.groupby([index, columns])[tgt_name].agg(['sum', 'count']).reset_index()
                    # 格子中客户数量小于阈值的，置为空
                    zero_index = (data['count'] < (data['count'].sum() / data.shape[0] * self.min_r)) | (data['count'] < self.min_count)
                    data.loc[zero_index, 'sum'] = 0

                    data['p'] = data['sum'] / data['count']
                    assert self.cmap_type in {'p', 'count'}
                    if self.cmap_type == 'p':
                        xdf = data.pivot(index=index, columns=columns, values='p')
                        xdf1 = data.pivot(index=index, columns=columns, values='sum')
                    else:
                        xdf1 = data.pivot(index=index, columns=columns, values='p')
                        xdf = data.pivot(index=index, columns=columns, values='sum')
                        
                    try:
                        xdf.sort_values(index, ascending=False, inplace=True)
                        xdf1.sort_values(index, ascending=False, inplace=True)
                    except:
                        warnings.warn('Sort xdf failed')
                    sns.heatmap(xdf, linewidths =0.01, cmap='Blues')
                    ax = plt.gca()
                    mesh = ax.pcolormesh(xdf, cmap=mpl.cm.get_cmap('Blues'))
                    _annotate_heatmap(plt, xdf1, ax, mesh, height=xdf.shape[0], width=xdf.shape[1], fmt=self.fmt)
                    
                sns.despine(left=True)
        # 对连续值绘制映射关系
        for j, columns in enumerate(fea_list):
            plt.subplot(nrows, ncols, (nrows-1)*ncols+j+1)
            if columns in self.dense_list:
                plt.text(0.2, 0.2, dense_fea_map[columns])
            else:
                plt.plot([])
            plt.xticks([])
            plt.xlabel('')
            plt.yticks([])
            plt.ylabel('')
            
        if self.title != '':
            plt.suptitle(self.title)
        plt.tight_layout()
        
        if self.save_path:
            # 保存文件
            save_dir = '/'.join(self.save_path.split('/')[:-1])
            save_file = self.save_path.split('/')[-1].split('.')[0] + '.jpg'
            os.makedirs(save_dir, exist_ok=True)
            plt.savefig(os.path.join(save_dir, save_file), dpi=100, bbox_inches='tight')

        return df_X, df_y, tracker


def _annotate_heatmap(plt, data, ax, mesh, height, width, fmt='.3f'):
    """Add textual labels with the value in each cell."""
    mesh.update_scalarmappable()
    xpos, ypos = np.meshgrid(np.arange(width) + .5, np.arange(height) + .5)
    for x, y, m, color, val in zip(xpos.flat, ypos.flat, mesh.get_array(), mesh.get_facecolors(), data.values.flat):
        lum = relative_luminance(color)
        text_color = ".15" if lum >.408 else "w"
        annotation = ("{:" + fmt + "}").format(val)
        text_kwargs = dict(color=text_color, ha="center", va="center")
        ax.text(x, y, annotation, **text_kwargs)


def relative_luminance(color):
    rgb = mpl.colors.colorConverter.to_rgba_array(color)[:, :3]
    rgb = np.where(rgb <= .03928, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    lum = rgb.dot([.2126, .7152, .0722])
    try:
        return lum.item()
    except ValueError:
        return lum
