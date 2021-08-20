import pandas as pd



# df = pd.read_table(r'C:\Users\dell\Desktop\崔佬\数据.csv',encoding='GB18030',low_memory=False)
import jieba
import re

result = []

def read_data():
    with open(r"C:\Users\pdcfi\Desktop\淘宝数据分析\淘宝商品3.csv") as f:
        for line in f:
            row = dict(re.findall("([^：\t]+)：([^：\t]+)", line))
            if row:
                result.append(row)
    df = pd.DataFrame(result)
    return df

# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='gbk').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stop_word.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

def get_data(df):
    # 将食品添加剂这一列空的数据设置为无
    # print(df)
    df.loc[:,'食品添加剂'] = df['食品添加剂'].fillna('无')
    df.loc[:,'保质期'] = df['保质期'].fillna('无')
    df.loc[:, '配料表'] = df['配料表'].fillna('无')

    #  分词并扩展提取
    # names=df.配料表.apply(lambda x: list(jieba.cut(x))).explode()
    # outputs = open('outputs.txt', 'w', encoding='gbk')
    # for data in names:
    #     line_seg = seg_sentence(data)  # 这里的返回值是字符串
        # outputs.write(line_seg + '\n')
    # outputs.close()
    # inputs = open('all_lyrics.txt', 'r', encoding='gbk')

    # for line in inputs:
    #     line_seg = seg_sentence(line)  # 这里的返回值是字符串
    #     outputs.write(line_seg + '\n')

    #  过滤长度小于等于1的词并去重
    names = df.配料表.apply(jieba.lcut).explode()
    df1 = names[names.apply(len) > 1].value_counts()

    with pd.ExcelWriter("taobao.xlsx") as writer:
        df1.to_excel(writer, sheet_name='配料')

    df2 = pd.read_excel('taobao.xlsx', header=None, skiprows=1, names=['column1', 'column2'])
    print(df2)


if __name__ == '__main__':
    df =read_data()
    get_data(df)



    # 查看单个series的平均值
    #
    # print(df['fengxiang'].unique())  # 包含的数据
    #
    # df2 = df['fengxiang'].value_counts()
    # with pd.ExcelWriter("test.xlsx") as writer:
    #     df.to_excel(writer, sheet_name="Sheet1")
    #     df2.to_excel(writer, sheet_name="Sheet2")














# import pandas as pd
# from pyecharts.charts import Bar
# df1 = pd.read_excel(r'C:\Users\dell\Desktop\崔佬\数据分析综合实战\new.xlsx',sheet_name=1)
# # df2 = pd.read_excel(r'C:\Users\dell\Desktop\崔佬\数据分析综合实战\new.xlsx',sheet_name=2)

# print(df1)
# # df1 = df['厂名'].value_counts()
# # df2 = df['保质期'].value_counts()
# # df3 = df['储藏方法'].value_counts()
# from pyecharts.charts import Bar
# from pyecharts import options as opts
#
#
# #
# a = df1['保质期'].to_list()
# print(a)
# b = df1['数值'].to_list()
# print(b)
#
# from pyecharts.charts import Pie
# from pyecharts import options as opts
#
#
# # 链式调用
# pie = (
#     Pie()
#     .add('',[list(z) for z in zip(a,b)],
#          radius=["30%","70%"],  # 半径长度
#          rosetype="radius"  # 扇区圆心角展现数据的百分比，半径展现数据的大小
#          )
#         .set_global_opts(title_opts=opts.TitleOpts(title="淘宝案例", subtitle="我是副标题"))
#         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))  # 数字项名称和百分比
#
#
# )
# pie.render('饼状图实例.html')

