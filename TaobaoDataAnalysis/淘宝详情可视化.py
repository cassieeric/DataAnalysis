import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
import jieba
import re


"""正则处理原始数据细分列  数据清洗剔除无用数据 返回清洗好的df"""
def read_data():
    result = []
    with open(r"C:\Users\pdcfi\Desktop\淘宝数据分析\淘宝商品3.csv") as f:
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
    with pd.ExcelWriter("淘宝商品配料数据.xlsx") as writer:
        df1.to_excel(writer, sheet_name="配料")
    fpath = r'C:\Users\pdcfi\Desktop\淘宝数据分析\淘宝商品配料数据.xlsx'
    # 读取数据 提取列
    df1 = pd.read_excel(fpath, header=None, skiprows=1, sheet_name='配料', names=['sx', 'sl'])
    a = df1['sx'].to_list()[:10]
    b = df1['sl'].to_list()[:10]

    from pyecharts.charts import Pie
    from pyecharts import options as opts
    # 绘制可视化图表
    pie = (
        Pie().add('', [list(z) for z in zip(a, b)],
                 radius=["20%", "60%"],  # 半径长度
                 rosetype="radius"  # 扇区圆心角展现数据的百分比，半径展现数据的大小
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title="淘宝商品数据配料统计", subtitle="8.19"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))  # 数字项名称和百分比

    )
    pie.render('淘宝商品数据配料统计.html')


"""生成保质期可视化图表"""
def get_date_html(df):
    # 词表分词
    names = df.保质期.apply(jieba.lcut).explode()
    df1 = names[names.apply(len) > 1].value_counts()
    # 写入分词后的结果
    with pd.ExcelWriter("淘宝商品保质期数据.xlsx") as writer:
        df1.to_excel(writer, sheet_name="保质期")
    fpath = r'C:\Users\pdcfi\Desktop\淘宝数据分析\淘宝商品保质期数据.xlsx'
    # 读取数据 提取列
    df1 = pd.read_excel(fpath, header=None, skiprows=1, names=['bzq', 'rq'])
    a = df1['bzq'].to_list()[:10]
    b = df1['rq'].to_list()[:10]
    from pyecharts.charts import Pie
    from pyecharts import options as opts
    # 绘制可视化图表
    pie = (
        Pie()
            .add('', [list(z) for z in zip(a, b)],
                 radius=["20%", "60%"],  # 半径长度
                 rosetype="radius"  # 扇区圆心角展现数据的百分比，半径展现数据的大小
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title="淘宝商品保质期可视化图表", subtitle="8.19"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))  # 数字项名称和百分比

    )
    pie.render('淘宝商品保质期统计.html')


if __name__ == '__main__':
    df =read_data()
    # get_data(df)
    get_date_html(df)
    get_ingredients_html(df)

