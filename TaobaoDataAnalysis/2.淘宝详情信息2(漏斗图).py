import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
import jieba
import re

from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker
from pyecharts.options import ComponentTitleOpts
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Funnel
from pyecharts.faker import Faker
import random
from pyecharts import options as opts
from pyecharts.charts import Polar

"""正则处理原始数据细分列  数据清洗剔除无用数据 返回清洗好的df"""
def read_data():
    result = []
    with open(r"C:\Users\dell\Desktop\崔佬\淘宝商品3.csv") as f:
        # 使用正则匹配数据
        for line in f:
            row = dict(re.findall("([^：\t]+)：([^：\t]+)", line))
            if row:
                result.append(row)
    df = pd.DataFrame(result)
    # 数据清洗 将食品添加剂这一列空的数据设置为无

    df.loc[:,'食品添加剂'] = df['食品添加剂'].fillna('无')
    df.loc[:,'保质期'] = df['保质期'].fillna('无')
    df.loc[:, '配料表'] = df['配料表'].fillna('无')
    return df



# 生成配料图表
def get_ingredients_html(df):
    # 词表分词
    names = df.配料表.apply(jieba.lcut).explode()
    df1 = names[names.apply(len)>1].value_counts()
    # 写入分词后的结果
    with pd.ExcelWriter("淘宝数据.xlsx") as writer:
        df1.to_excel(writer, sheet_name="配料")
    fpath = r'C:\Users\dell\Desktop\崔佬\数据分析综合实战\淘宝数据.xlsx'
    # 读取数据 提取列
    df1 = pd.read_excel(fpath,header=None,skiprows=1,sheet_name='配料',names=['sx','sl'])
    a = df1['sx'].to_list()[:10]
    b = df1['sl'].to_list()[:10]

    from pyecharts.charts import Pie
    from pyecharts import options as opts
    # 绘制可视化图表
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
            .add('', [list(z) for z in zip(a, b)],
                 radius=["20%", "60%"],  # 半径长度
                 rosetype="radius"  # 扇区圆心角展现数据的百分比，半径展现数据的大小
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title="配料统计", subtitle="8.19"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))  # 数字项名称和百分比

    )
    return pie


"""生成保质期可视化图表"""
def get_date_html(df):
    # 词表分词
    names = df.保质期.apply(jieba.lcut).explode()
    df1 = names[names.apply(len) > 1].value_counts()
    # 写入分词后的结果
    with pd.ExcelWriter("淘宝数据.xlsx") as writer:
        df1.to_excel(writer, sheet_name="保质期")
    fpath = r'C:\Users\dell\Desktop\崔佬\数据分析综合实战\淘宝数据.xlsx'
    # 读取数据 提取列
    df1 = pd.read_excel(fpath, header=None, skiprows=1, names=['bzq', 'rq'])
    a = df1['bzq'].to_list()[:50]
    b = df1['rq'].to_list()[:50]

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
            .add_xaxis(a)
            .add_yaxis("保质期(天数)",b)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-保质期）"),
            datazoom_opts=opts.DataZoomOpts(),
        )

    )
    return bar
    # 链式调用
    # bar = (
    #     Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
    #         # 添加x的数据
    #         .add_xaxis(a)
    #         .add_yaxis('电商渠道', b)
    #         .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
    #                          markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最大值"), ]))
    #         .set_global_opts(title_opts=opts.TitleOpts(title='保质期', subtitle='2021年八月'),)
    # )
    #
    # bar.render('dianshang.html')
    # bar.render_notebook()
    # return bar


def get_table(df):
    # 词表分词
    names = df.配料表.apply(jieba.lcut).explode()
    df1 = names[names.apply(len) > 1].value_counts()
    # 写入分词后的结果
    with pd.ExcelWriter("淘宝数据.xlsx") as writer:
        df1.to_excel(writer, sheet_name="配料")
    fpath = r'C:\Users\dell\Desktop\崔佬\数据分析综合实战\淘宝数据.xlsx'
    # 读取数据 提取列
    df1 = pd.read_excel(fpath, header=None, skiprows=1, names=['配料表', '数据'])

    table = Table()
    headers = df.columns.to_list()
    rows = df.values.tolist()
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="Table-基本示例", subtitle="我是副标题支持换行哦")
    )
    return table


def get_table2(df):
    # 词表分词
    names = df.配料表.apply(jieba.lcut).explode()
    df1 = names[names.apply(len) > 1].value_counts()
    # 写入分词后的结果
    with pd.ExcelWriter("淘宝数据.xlsx") as writer:
        df1.to_excel(writer, sheet_name="配料")
    fpath = r'C:\Users\dell\Desktop\崔佬\数据分析综合实战\淘宝数据.xlsx'
    # 读取数据 提取列
    df1 = pd.read_excel(fpath, header=None, skiprows=1, names=['配料表', '数据'])

    table = Table()
    headers = df1.columns.to_list()[:10]
    rows = df1.values.tolist()[:10]
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="商品配料频率统计", subtitle="小小明大佬yyds")
    )
    return table



def get_sptj_data(df):
    # 词表分词
    names = df.食品添加剂.apply(jieba.lcut).explode()
    df1 = names[names.apply(len) > 1].value_counts()
    # 写入分词后的结果
    with pd.ExcelWriter("淘宝数据.xlsx") as writer:
        df1.to_excel(writer, sheet_name="食品添加剂")
    fpath = r'C:\Users\dell\Desktop\崔佬\数据分析综合实战\淘宝数据.xlsx'
    # 读取数据 提取列
    df1 = pd.read_excel(fpath, header=None, skiprows=1, names=['sptj', 'sj'])
    a = df1['sptj'].to_list()[:10]
    b = df1['sj'].to_list()[:10]
    c = (
        Funnel(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
            .add(
            "商品",
            [list(z) for z in zip(a, b)],
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Funnel-Label（food_add)"))
    )
    return c





def zb_data():
    data = [(i, random.randint(1, 100)) for i in range(10)]
    c = (
        Polar()
        .add(
            "",
            data,
            type_="effectScatter",
            effect_opts=opts.EffectOpts(scale=10, period=5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Polar-没啥用，用来装逼，小小明yyds"))

    )
    return c





def page_draggable_layout(df):
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        get_ingredients_html(df),
        get_date_html(df),
        get_sptj_data(df),
        zb_data(),
        get_table2(df),
        get_table(df)
    )
    page.render("page_draggable_layout.html")
    print('ok')






if __name__ == '__main__':
    df =read_data()
    # get_data(df)
    page_draggable_layout(df)

