# 可以使用 Python 中的 docx 和 openpyxl 库实现该功能，具体步骤如下：
#
# 1. 使用 docx 库读取 word 文档中的所有文本，并将其存入一个字符串中。
#
# 2. 使用 jieba 分词库对文本进行分词处理，并过滤掉无用词汇。
#
# 3. 利用 Python 中的 Collection 库的 Counter 类，统计每个单词的词频。
#
# 4. 使用 Python 中的 NLTK 库对每个单词进行词性标注，将其存入一个字典中。
#
# 5. 使用 openpyxl 库创建一个 Excel 文件，并在其中创建一个工作表。
#
# 6. 将关键词、词性和词频分别写入文件的不同列中。
#
# 下面是可能的实现代码：


import docx
import jieba
from collections import Counter
import openpyxl
from openpyxl import Workbook
from nltk import pos_tag

# 读取 word 文档中的内容
doc = docx.Document('武汉红色之旅观后感_彭东成.docx')
text = ""
for para in doc.paragraphs:
    text += para.text

# 对文本进行分词，并过滤无意义单词
words = [word for word in jieba.cut(text) if len(word) > 1 and not word.isnumeric()]

# 统计单词词频
word_counts = Counter(words)

# 对每个单词进行词性标注
pos_dict = dict(pos_tag(word_counts.keys()))

# 将关键词、词性、词频存入列表中
keywords = []
for word, count in word_counts.items():
    pos = pos_dict[word]
    keywords.append([word, count, pos])

# 创建 Excel 文件
wb = Workbook()
sheet = wb.active

# 将关键词、词性、词频写入 Excel 文件
sheet['A1'] = '关键词'
sheet['B1'] = '词频'
sheet['C1'] = '词性'
for i, row in enumerate(keywords):
    sheet['A{}'.format(i+2)] = row[0]
    sheet['B{}'.format(i+2)] = row[1]
    sheet['C{}'.format(i+2)] = row[2]

# 保存 Excel 文件
wb.save('keywords.xlsx')

