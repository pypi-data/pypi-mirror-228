import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class SankeyOne(object):
    def __init__(self, labels, figsize=(10,8), name='sankey_one', title='', save_path=None, pipeline_return=False, 
                 offset=10, fontsize=12, height=0.25, **kwargs):
        '''桑基图
        '''
        self.labels = labels
        self.save_path = save_path
        self.name = name
        self.figsize = figsize
        self.title = title
        self.pipeline_return = pipeline_return
        self.height = height
        self.fontsize = fontsize
        self.offset = offset
        
    def fit(self, df_X, df_y=None, **tracker):
        df = df_X.copy()
        
        # 找到不同label对应的数量
        x1 = []
        for label in self.labels:
            # 如果传入了all_users, 则该层增加所有用户
            if label == 'all_users':
                x1.append(df.shape[0])
                continue
            sel_col = ''
            for col in df.columns:
                if col in label:
                    if len(col) > len(sel_col):
                        sel_col = col
            if sel_col == '':
                raise ValueError(f'`{label}` not in dataframe columns')
            sel_row = eval(label.replace(sel_col, f'df["{sel_col}"]'))
            # bool型意味着该label存在=, <等符号
            if sel_row.dtype == 'bool':
                df = df.loc[sel_row]
            x1.append(df.shape[0])
        x1 = np.array(x1)
        x2 = np.array((x1.max()-x1)/2)
        x3 = [i+j for i,j in zip(x1,x2)]
        x3 = np.array(x3)
        y = -np.sort(-np.arange(len(self.labels)))
        fig = plt.figure(figsize = self.figsize)
        ax = fig.add_subplot(111)
        rects1 = ax.barh(y, x3, self.height, tick_label=self.labels, color='g', alpha=0.5)
        rects2 = ax.barh(y, x2, self.height, color='w', alpha=1)
        ax.plot(x3, y, 'w', alpha=0.7)
        ax.plot(x2, y, 'w', alpha=0.7)
        notes = []
        for i in range(0, len(x1)):
            notes.append(f'{x1[i]} | ' + '%.2f%%'%((x1[i]/x1[0])*100))
        for rect_one, rect_two, note in zip(rects1, rects2, notes):
            text_x = rect_two.get_width() + (rect_one.get_width() - rect_two.get_width())/2 - self.offset
            text_y = rect_one.get_y() + self.height/2
            ax.text(text_x, text_y, note, fontsize=self.fontsize)
        ax.set_xticks([])
        for direction in ['top','left','bottom','right']:
            ax.spines[direction].set_color('none')
        ax.yaxis.set_ticks_position('none')
        plt.title(self.title)
        plt.show()

        if self.save_path:
            # 保存文件
            save_dir = '/'.join(self.save_path.split('/')[:-1])
            save_file = self.save_path.split('/')[-1].split('.')[0] + '.jpg'
            os.makedirs(save_dir, exist_ok=True)
            plt.savefig(os.path.join(save_dir, save_file), dpi=100, bbox_inches='tight')
        
        if self.pipeline_return:
            df_y = tracker.pop('df_y') if 'df_y' in tracker else None
            return df_X, df_y, tracker
        else:
            return


class Sankey(object):
    def __init__(self, labels, save_path, name='sankey', count_label=None, pipeline_return=False, bin_count=10, title='桑基图',
                 title_pos='center',  title_top='top', title_color='#595959', title_text_size=30,
                 width=1800,  height=600, line_opacity=0.2, line_curve=0.6, line_width=15,
                 line_color="gray", is_label_show=True, sankey_node_width=30, sankey_node_gap=8,
                 label_text_size=20, label_pos="right", max_bins=10, **kwargs):
        '''桑基图
        对于离散变量直接拆分，对于连续型变量则qcut后进行拆分，如拆分不对可以在外部拆分好
        labels: list(str), 需要参加绘制的列
        save_path: str, 最后保存为了html文件，在jupyter中预览不了，因此要求传入save_path
        count_label: str, 表示count的列名，如果为None，表示按照count_label来统计数量
        title=self.title,#主标题名称
        title_pos='center',#主标题距离左侧距离，有’auto’, ‘left’, ‘right’, 'center’可选，也可为百分比或整数
        title_top='top',#主标题距离顶部距离，有’top’, ‘middle’, 'bottom’可选，也可为百分比或整数
        title_color='#595959',#主标题文本颜色，颜色的取值直接输入英文单词也可支持；十六进制大小写均可。
        title_text_size=30,#主标题文本字体大小
        width=1800,#设置图的宽度
        height=600#设置图的高度
        line_opacity=0.2,#曲线色彩深度
        line_curve=0.6,#曲线弧度
        line_width=15,#曲线宽度
        line_color="gray",#设置转态转化之间连接线的颜色，可以填写颜色，也可以设置为target或source
        is_label_show=True,#是否显示标签
        sankey_node_width=30,#各节点的宽度
        sankey_node_gap=8,#同列上下节点之间的距离
        label_text_size=20,#设置标签字体大小
        label_pos="right",#标签位置，可以设置靠左或者靠右
        max_bins=10, # 最大的箱体个数
        '''
        assert len(labels) > 1, "Sankey only supports 2 columns above"
        self.labels = labels
        self.save_path = '.'.join(save_path.split('.')[:-1]) + '.html'
        self.title = title
        self.count_label = count_label
        self.name = name
        self.pipeline_return = pipeline_return
        self.bin_count = bin_count

        self.title_pos = title_pos
        self.title_top = title_top
        self.title_color = title_color
        self.title_text_size = title_text_size
        self.width = width
        self.height = height
        self.line_opacity = line_opacity
        self.line_curve = line_curve
        self.line_width = line_width
        self.line_color = line_color
        self.is_label_show = is_label_show
        self.sankey_node_width = sankey_node_width
        self.sankey_node_gap = sankey_node_gap
        self.label_text_size = label_text_size
        self.label_pos = label_pos
        self.max_bins = max_bins
        
    def fit(self, df_X, df_y=None, **tracker):
        if self.count_label is None:
            df = df_X[self.labels].copy()
        else:
            df = df_X[self.labels + [self.count_label]].copy()
        from pyecharts import Sankey

        nodes = []
        for col in self.labels:
            # 数值型数量过大时候，需要切分
            if df[col].nunique() > self.max_bins: 
                if (df[col].dtype == float) or (df[col].dtype == int):
                    df[col] = pd.qcut(df[col], q=self.bin_count, duplicates='drop', retbins=True)[0].astype(str)
                else:
                    raise ValueError(f'Column {col} has {df[col].nunique()} categories which is above threthold {self.max_bins}')

            df[col] = df[col].astype(str).fillna('nan')
            nodes.extend([{'name': f'{col}={item}'} for item in df[col].unique()])

        links = []
        for i, index in enumerate(self.labels[:-1]):
            columns = self.labels[i+1]
            if self.count_label is None:
                data = df.groupby([index, columns]).size().reset_index(name='__count')
            else:
                data = df.groupby([index, columns])[self.count_label].sum().reset_index(name='__count')
            
            xdf = data.pivot(index=index, columns=columns, values='__count')
            for row in xdf.index:
                for col in xdf.columns:
                    if ~np.isnan(xdf.loc[row, col]):
                        links.append({'source': f'{index}={row}', 'target': f'{columns}={col}', 'value': xdf.loc[row, col]})

        snakey = Sankey(
                title=self.title,#主标题名称
                title_pos=self.title_pos,#主标题距离左侧距离，有’auto’, ‘left’, ‘right’, 'center’可选，也可为百分比或整数
                title_top=self.title_top,#主标题距离顶部距离，有’top’, ‘middle’, 'bottom’可选，也可为百分比或整数
                title_color=self.title_color,#主标题文本颜色，颜色的取值直接输入英文单词也可支持；十六进制大小写均可。
                title_text_size=self.title_text_size,#主标题文本字体大小
                width=self.width,#设置图的宽度
                height=self.height#设置图的高度
        )
        snakey.add(
            "",#按钮，用来控制是否显示图标。若不显示，可以设置为‘空格’，不能缺省。
            nodes,#输入节点
            links,#输入关系
            line_opacity=self.line_opacity,#曲线色彩深度
            line_curve=self.line_curve,#曲线弧度
            line_width=self.line_width,#曲线宽度
            line_color=self.line_color,#设置转态转化之间连接线的颜色，可以填写颜色，也可以设置为target或source
            is_label_show=self.is_label_show,#是否显示标签
            sankey_node_width=self.sankey_node_width,#各节点的宽度
            sankey_node_gap=self.sankey_node_gap,#同列上下节点之间的距离
            label_text_size=self.label_text_size,#设置标签字体大小
            label_pos=self.label_pos,#标签位置，可以设置靠左或者靠右
        )
        snakey.render(self.save_path)

if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame(np.random.rand(1000, 10))
    for i in range(5):
        df[i] = np.random.randint(2, 10, 1000)
    df.columns = [f'fea_{i}' for i in range(df.shape[1])]
    df['target'] = np.random.randint(0, 2, 1000)

    df.loc[0, 'fea_0'] = np.nan
    sankey = Sankey(labels=['fea_0', 'fea_1'], save_path='./tmp.html')
    sankey.fit(df)


    # =======================pyechart绘制桑基图
    from pyecharts import Sankey
    nodes = [
        {'name': '创建订单-1828'}, {'name': '未支付-935'}, {'name': '已支付-893'},
        {'name': '未发货-114'}, {'name': '已发货-779'}, {'name': '未收货-111'},
        {'name': '已收货-669'}, {'name': '未删除-813'}, {'name': '已删除-122'},
        {'name': '已退款-51'}, {'name': '未退款-65'}, {'name': '待收货-109'}, {'name': '订单完成-601'},
    ]#此处罗列各分支名称，后面的数字代表具体的量值(注：因为pyecharts无法直接显示value，所以需要这样标注)。
    links = [
        {'source': '创建订单-1828', 'target': '未支付-935', 'value': 935},
        {'source': '创建订单-1828', 'target': '已支付-893', 'value': 893},
        {'source': '未支付-935', 'target': '未删除-813', 'value': 813},
        {'source': '未支付-935', 'target': '已删除-122', 'value': 122},
        {'source': '已支付-893', 'target': '未发货-114', 'value': 114},
        {'source': '已支付-893', 'target': '已发货-779', 'value': 779},
        {'source': '未发货-114', 'target': '已退款-51', 'value': 49},
        {'source': '未发货-114', 'target': '未退款-65', 'value': 65},
        {'source': '已发货-779', 'target': '未收货-111', 'value': 111},
        {'source': '已发货-779', 'target': '已收货-669', 'value': 668},
        {'source': '未收货-111', 'target': '待收货-109', 'value': 109},
        {'source': '未收货-111', 'target': '已退款-51', 'value': 2},
        {'source': '已收货-669', 'target': '订单完成-601', 'value': 601},
    ]#此处罗列各分支之间的关联关系，source表示节点，target表示终点，value表示状态转化的量值。

    snakey = Sankey(
            title="订单状态转化图",#主标题名称
            title_pos='center',#主标题距离左侧距离，有’auto’, ‘left’, ‘right’, 'center’可选，也可为百分比或整数
            title_top='top',#主标题距离顶部距离，有’top’, ‘middle’, 'bottom’可选，也可为百分比或整数
            title_color='#595959',#主标题文本颜色，颜色的取值直接输入英文单词也可支持；十六进制大小写均可。
            title_text_size=30,#主标题文本字体大小
            width=1800,#设置图的宽度
            height=600#设置图的高度
    )
    snakey.add(
        "",#按钮，用来控制是否显示图标。若不显示，可以设置为‘空格’，不能缺省。
        nodes,#输入节点
        links,#输入关系
        line_opacity=0.2,#曲线色彩深度
        line_curve=0.6,#曲线弧度
        line_width=15,#曲线宽度
        line_color="gray",#设置转态转化之间连接线的颜色，可以填写颜色，也可以设置为target或source
        is_label_show=True,#是否显示标签
        sankey_node_width=30,#各节点的宽度
        sankey_node_gap=8,#同列上下节点之间的距离
        label_text_size=20,#设置标签字体大小
        label_pos="right",#标签位置，可以设置靠左或者靠右
    )
    snakey.render()
