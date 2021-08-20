# 手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示

## 一、前言

​	大家好，我是Python进阶者，上个礼拜的时候，我的Python交流群里有个名叫程序的大佬，头像是绿色菜狗的那位，在Python交流群里边的人应该都知道我说的是哪个大佬了，他提供了一份初始淘宝数据，数据乍看上去非常杂乱无章，但是经过小小明大佬的神化处理之后，一秒就变清晰了，真是太神了，然后就有了后续的数据分词处理和可视化等内容了，可能群里的人平时工作太忙，没有来得及看群消息，作为热心的群主，这里给大家整理成一篇文章，感兴趣的小伙伴，可以去实操一下，还是可以学到很多东西的。言归正传，一起来学习下今天的数据分析内容吧。



## 二、原始数据预处理

### 	1、原始数据

​	在未经过处理之前的数据，长这样，大家可以看看，全部存储在一个单元格里边了，看得十分的让人难受。如下图所示。

![image-20210819204701769](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819204701769.png)

​	按照常规来说，针对上面的数据，我们肯定会选择Excel里边的数据分列进行处理，然后依次的去根据空格、冒号去分割，这样可以得到一份较为清晰的数据表，诚然，这种方法确实可行，但是小小明大佬另辟蹊径，给大家用Python中的正则表达式来处理这个数据，处理方法如下。

### 	2、原始数据预处理

​	小小明大佬直接使用正则表达式re模块和pandas模块进行处理，方法可谓巧妙，一击即中，数据处理代码如下。

```Python
import re
import pandas as pd
result = []
with open(r"淘宝数据.csv") as f:
    for line in f:
        row = dict(re.findall("([^：\t]+)：([^：\t]+)", line))
        if row:
            result.append(row)
df = pd.DataFrame(result)
df.to_excel('new_data.xlsx', encoding='utf-8')
print(df)

```

​	之后我们可以看到效果图，如下图所示，这下是不是感觉到清爽了很多呢？

![image-20210819205508029](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819205508029.png)

​	至此，我们对原始的数据进行了预处理，但是这还不够，我们今天主要的目标是对上面数据中的两列：配料表和保质期进行数据分析，接下来继续我们的数据处理和分析。

## 三、对配料表和保质期列进行处理

​	一开始的时候，程序大佬对配料表和保质期这两列的数据进行处理，但是来回得到的分词中总有一些特殊字符，如下图所示，我们可以看到这些字符里边有%、顿号、空格等内容。

![image-20210819210206439](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819210206439.png)

​	我们都知道，这些是我们不需要的字符，当时我们在群里讨论的时候，我们就想到使用停用词去针对这些扰人的字符进行处理，代码如下。

```python
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
```

​	其中stop_word.txt是小编之前在网上找到的一个存放一些常用特殊字符的txt文件，这个文件内容可以看看下图。

![image-20210819210555283](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819210555283.png)

​	如上图所示，大概有1894个词左右，其实在做词频分析的时候，使用停用词去除特殊字符是经常会用到的，感兴趣的小伙伴可以收藏下，也许后面你会用到呢？代码和数据我统一放到文末了，记得去取就行。经过这一轮的数据处理之后，我们得到的数据就基本上没有太多杂乱的字符了，如下图所示。

![image-20210819210945732](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819210945732.png)

​	得到这些数据之后，接下来我们需要对这些词语做一些词频统计，并且对其进行可视化。如果还有想法的话，也可以直接套用词云模板，生成漂亮的词云图，也未尝不可。

## 四、词频统计

​	关于词频统计这块，小编这里介绍两种方法，两个代码都是可以用的，条条大路通罗马，一起来看看吧！

### 方法一：常规处理

​	这里使用的是常规处理的方法，代码亲测可用，只需要将代码中的1.txt进行替换成你自己的那个需要分词统计的文档即可，然后系统会自动给你生成一个Excel表格和一个TXT文件，内容都是一样的，只不过一个是表格，一个是文本。

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import jieba
import jieba.analyse
import xlwt  # 写入Excel表的库

# reload(sys)
# sys.setdefaultencoding('utf-8')

if __name__ == "__main__":

    wbk = xlwt.Workbook(encoding='ascii')
    sheet = wbk.add_sheet("wordCount")  # Excel单元格名字
    word_lst = []
    key_list = []
    for line in open('1.txt', encoding='utf-8'):  # 1.txt是需要分词统计的文档

        item = line.strip('\n\r').split('\t')  # 制表格切分
        # print item
        tags = jieba.analyse.extract_tags(item[0])  # jieba分词
        for t in tags:
            word_lst.append(t)

    word_dict = {}
    with open("wordCount_all_lyrics.txt", 'w') as wf2:  # 打开文件

        for item in word_lst:
            if item not in word_dict:  # 统计数量
                word_dict[item] = 1
            else:
                word_dict[item] += 1

        orderList = list(word_dict.values())
        orderList.sort(reverse=True)
        # print orderList
        for i in range(len(orderList)):
            for key in word_dict:
                if word_dict[key] == orderList[i]:
                    wf2.write(key + ' ' + str(word_dict[key]) + '\n')  # 写入txt文档
                    key_list.append(key)
                    word_dict[key] = 0

    for i in range(len(key_list)):
        sheet.write(i, 1, label=orderList[i])
        sheet.write(i, 0, label=key_list[i])
    wbk.save('wordCount_all_lyrics.xls')  # 保存为 wordCount.xls文件
```



### 	2、方法二：使用Pandas优化处理

​	这里使用Pandas方法进行处理，代码如下，小编也是亲测有效，小伙伴们也可以去尝试下。

```python
def get_data(df):
    # 将食品添加剂这一列空的数据设置为无
    # print(df)
    df.loc[:,'食品添加剂'] = df['食品添加剂'].fillna('无')
    df.loc[:,'保质期'] = df['保质期'].fillna('无')
    df.loc[:, '配料表'] = df['配料表'].fillna('无')

    #  分词并扩展提取
    names = df.配料表.apply(jieba.lcut).explode()
    #  过滤长度小于等于1的词并去重
    df1 = names[names.apply(len) > 1].value_counts()

    with pd.ExcelWriter("taobao.xlsx") as writer:
        df1.to_excel(writer, sheet_name='配料')

    df2 = pd.read_excel('taobao.xlsx', header=None, skiprows=1, names=['column1', 'column2'])
    print(df2)
```

​	上面两个代码都是可以用的，最后得到的表格数据，如下图所示。

![image-20210819211833115](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819211833115.png)

​	从上图我们可以看到配料表里边的配料占比详情，有了上述的数据之后，接下来我们就可以对其进行可视化操作了。

## 五、可视化

​	可视化部分，我们采用Pyecharts库来进行完成，这个库作图十分的炫酷，而且可以交互，十分带感，强烈推荐。关于这部分，小编以生成配料图表和生成保质期可视化图表为例来进行展开。

### 1、生成配料饼图

针对配料数据，我们使用一个饼图去进行展示，这样显得更加高大上一些，直接上代码。

```python
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
```

​	在Pycharm里边运行代码之后，我们将会得到一个淘宝商品数据配料统计.html文件，双击打开该HTML文件，在浏览器里边可以看到效果图，如下图所示。

![image-20210819212412409](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819212412409.png)

​	是不是感觉一下子就高大上了呢？而且动动鼠标，你还可以进行交互，是动态图来着，十分好玩。

### 2、生成保质期可视化饼图

​	针对保质期数据，我们也先使用一个饼图去进行展示，直接上代码，其实你会发现和上面那个配料图表大同小异。

```python
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
```

​	在Pycharm里边运行代码之后，我们将会得到一个淘宝商品保质期统计.html文件，双击打开该HTML文件，在浏览器里边可以看到效果图，如下图所示。

![image-20210819212713541](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819212713541.png)

​	相信有小伙伴肯定感觉哪里不对，一个保质期的可视化，做成这种饼图似乎太丑了吧？嗯，的确是丑爆了，所以程序大佬把保质期这个图转为了柱状图，这样看上去就高大上很多了。

### 3、生成保质期可视化柱状图

​	其实数据都是一样的，只不过呈现方式不同，直接上代码。

```python
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
```

​	这么处理之后，我们就会得到一个柱状图了，如下图所示。

![image-20210819213419570](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819213419570.png)

​	这把看上去，是不是觉得清晰很多了呢？

​	不过呢，程序大佬还觉得不够，想把这两张图放到一起，这应该怎么办呢？

### 4、合并饼图和柱状图到一个HTML文件

​	其实这个也并不难，只需要将生成两个图的函数放到一个布局类里边就可以完成了，直接上代码。

```python
def page_draggable_layout(df):
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        get_ingredients_html(df),
        get_date_html(df)
    )
    page.render("page_draggable_layout.html")
```

​	如果你想在一个HTML文件里边加入更多的图，只需要继续在add()函数里面进行添加生成可视化图的函数即可。话不多说，直接上效果图。

![image-20210819213942216](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819213942216.png)

​	从上图我们可以看到配料饼图和保质期柱状图都同时在同一个HTML文件出现了，而且也是可以进行点击交互的噢！我们还可以收到拖拽，让图表移动，如下图所示，分为左右图进行展示。

![image-20210819214025265](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819214025265.png)

​	你以为到这里就结束了？其实并没有，程序大佬还想玩点更加高大上的，他想把table表一并显示出来，这样显得更加饱满一些。那么table表又如何来进行显示呢？

### 5、table表加持

​	其实在这里，程序大佬卡了一下，他在群里问，基于他目前的数据，像下图这样的df数据如何进行展示出来。

![image-20210819214335851](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819214335851.png)

​	而且，他自己在不断的尝试中，始终报错，一时间丈二和尚摸不着头脑，不知如何是好。

![image-20210819214421686](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819214421686.png)

​	不过此时小小明大佬，又递来了橄榄枝，人狠话不多，直接丢了两行代码，让人拍手叫绝。

![image-20210819214853777](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819214853777.png)

​	然后程序大佬，拿到Pycharm中一跑，啪，成了，真是拍案叫绝，小小明yyds！那么呈现的效果图是下面这样的。

![image-20210819215038102](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819215038102.png)

这样看上去还稍微不太好看，拖拽下，调整下格式看看，如下图所示。

![image-20210819221452871](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819221452871.png)

​	但是这样一看，确实高大上了一些，不过还是达不到程序大佬心里的预期，于是乎他继续折腾。

### 6、调整图像背景色

​	现在呢，程序大佬又想要加点背景色，这样显得高大上一些，代码如下。

```python
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
```

其实核心的那句代码下面这个，引入了一个主题：

```python
init_opts=opts.InitOpts(theme=ThemeType.CHALK)
```

![image-20210819221641267](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819221641267.png)

​	得到的效果图如上图所示了。

### 7、添加漏斗图

​	这里是以数据里边的”食品添加“列来做实例的，代码如下所示。

```python
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
```

得到的效果图如下图所示。

![image-20210819222241463](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819222241463.png)

写到这里，基本上快接近尾声了，不过程序大佬为了感谢小小明大佬，后来又补充了一个极化装逼图来赞扬小小明。

### 8、极化图

​	直接上代码，程序大佬取的这个zb函数，就是装13的意思，取的太没有水平了。

```python
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
```

​	那么做出来的效果图就是下面这样的了，一起来膜拜下吧~

![image-20210819222646485](手把手教你用Pandas和Pyecharts库对淘宝数据进行数据处理和可视化展示.assets/image-20210819222646485.png)

​	看上去确实狠高大上呢。

## 六、总结

​	大家好，我是Python进阶者。本文写到这里，基本上就告一段落了。本文基于一份杂乱的淘宝原始数据，利用正则表达式re库和Pandas数据处理对数据进行清洗，然后通过stop_word停用词对得到的文本进行分词处理，得到较为”干净“的数据，之后利用传统方法和Pandas优化处理两种方式对数据进行词频统计，针对得到的数据，利用Pyecharts库，进行多重可视化处理，包括但不限于饼图、柱状图、Table表、漏斗图、极化图等，通过一系列的改进和优化，一步步达到想要的效果，可以说是干货满满，实操性强，亲测有效。

​	最后非常感谢程序大佬和小小明大佬在期间不断提供的代码，也感谢我自己花时间和心思把这些看似杂乱的消息整理成文，分享给大家学习。有需要本文中完整代码文件的小伙伴，可以在后台直接回复关键词”**程序和小小明大佬**“即可获取。

​	我的这个Python交流群已经300多人了，有需要加入该群的小伙伴可以加我好友，一起学习，共同进步。

