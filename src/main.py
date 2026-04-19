import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from apyori import apriori

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'docs', 'images')

# 确保输出目录存在
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 读取文件报utf-8错误，加encoding参数为gbk
GoodsOrder = pd.read_csv(os.path.join(DATA_DIR, "GoodsOrder.csv"), encoding='gbk')
# 查看表列数据类型
GoodsOrder.dtypes

# describe 描述性统计,默认统计数字类型数据
# 数字类型和字符串类型的描述性统计不一样
GoodsOrder['Goods'].describe()
'''
astype将类型转换
count     43367
unique     9835
top        1217
freq         32
Name: id, dtype: object
'''
# count为总共有多少行，unique为出现不同次数的总和，top显示次数最多，freq为top出现的次数
GoodsOrder['id'].astype(str).describe()

# value_counts为详细统计每个商品出现的次数，默认降序
# 排名前十的商品
num = GoodsOrder['Goods'].value_counts()[:10]

# matplotlib默认不支持中文所以把字体转换成黑体
plt.rcParams['font.sans-serif'] = 'SimHei'
# # bar是柱状图
# plt.bar(range(10), num)
# # 处理x横坐标,将range(10)修改成num.index，rotation将字体倾斜45度
# plt.xticks(range(10), num.index, rotation = 45)

# style.use更改图形样式
plt.style.use('ggplot')
# figure调节图像大小，清晰度
plt.figure(dpi = 1980)
# barh水平柱状图
plt.barh(num.index, num)
plt.title('商品销量排名前十的销售情况')
# xlabel为x轴的标题
plt.xlabel('销量')
# ylabel为y轴的标题
plt.ylabel('商品')
# 保存水平柱状图
plt.savefig(os.path.join(OUTPUT_DIR, '商品销量排名水平柱状图.png'), dpi=1980, bbox_inches='tight')
plt.show()


# 统计占比
GoodsOrder['Goods'].value_counts()/len(GoodsOrder['Goods'])


GoodsTypes = pd.read_csv(os.path.join(DATA_DIR, "GoodsTypes.csv"), encoding='gbk')
# merge数据融合,on是按照商品名称把它归总到一起，how为左连接还是右连接
# 给GoodsOrder表连接了GoodsTypes的Types列
data = pd.merge(GoodsOrder,GoodsTypes, on = 'Goods', how = 'left')
# 查看列
data.columns
# Types列出现次数排名
num = data['Types'].value_counts()
# 占比,round(2)为保留两位小数,apply为单独处理每个元素
num_rate = (num*100/len(data)).round(2)
# 将两个数据合并到一起,axis默认将新数据放置下边，axis=1为将num_rate数据放置右边
res = pd.concat([num, num_rate], axis = 1)
# 更改列名
res.columns = ['销量','销量占比']
# apply为单独处理每个元素
res['销量占比'] = res['销量占比'].apply(lambda x: str(x)+'%')

# pie为制作饼图,labels为添加名字，autopct为在饼图里添加数字
plt.pie(num, labels=num.index ,autopct='%.2f %%')
plt.title('各类别商品销售占比情况')
plt.savefig(os.path.join(OUTPUT_DIR, '各类别商品销售占比饼图.png'), dpi=1980, bbox_inches='tight')
plt.show()
'''
通过分析各类别商品的销量及其占比情况可知，
非酒精饮料、西点、果蔬三类商品销量差距不大，
占总销量的 50% 左右，同时，
根据大类 “分发现和食品相关的类的销量总和接近 90%，
说明了顾客们向于购买此类产品，
而其余商品仅为商场满足顾客的其余需求而设定，
并非销售的主力军。
'''




# 提取出非酒精饮料,输出满足条件的行数
tmp = data.loc[data['Types'] == '非酒精饮料']
# # value_counts为详细统计每个商品出现的次数，默认降序
num = tmp['Goods'].value_counts()

# 占比,round(2)为保留两位小数,apply为单独处理每个元素
num_rate = (num*100/len(tmp)).round(2)
# 将两个数据合并到一起,axis默认将新数据放置下边，axis=1为将num_rate数据放置右边
res = pd.concat([num, num_rate], axis = 1)
# 更改列名
res.columns = ['销量','销量占比']
# apply为单独处理每个元素
res['销量占比'] = res['销量占比'].apply(lambda x: str(x)+'%')

# 初始化全为0的偏移列表
explode = [0.04] * len(num)
# 对索引8、9、10（连续）设置偏移0.1
explode[8:11] = [0.2] * 3  # 切片8:11包含索引8、9、10

# figure为增大画布尺寸（从默认的(10,8)改为(12,10)，给扇形更多空间）
plt.figure(figsize=(12, 10))
# pie为制作饼图,labeldistance为文字离饼图的距离，explode为离散原点距离
plt.pie(num, labels=num.index ,autopct='%.2f %%', labeldistance=1.1, explode=explode)
plt.title('非酒精饮料的商品销售占比情况')
plt.savefig(os.path.join(OUTPUT_DIR, '非酒精饮料的商品销售占比饼图.png'), dpi=1980, bbox_inches='tight')
plt.show()

'''
通过分析非酒精饮料内部商品的销量及其占比情况可知，
全脂牛奶的销量在非酒精饮料的总销量中占比超过 33%，
前 3 种非酒精饮料的销量在非酒精饮料的总销量中占比接近 70%，
说明了大部分顾客到店购买的饮料为这三种，
需要时常注意货物的库存，定期补货必不可少。
'''




tmp = GoodsOrder.copy()
# apply为单独处理每个元素
tmp['Goods'] = tmp['Goods'].apply(lambda x: x+',')
# groupby为按照id列来分组求和
res = tmp.groupby('id').sum()
# 转换成Apriori前置需要的数据list
# 在apply中用split函数将两个元素以逗号的方式分割
# 正则re.sub函数去除（$为结尾）的空值
res = list(res['Goods'].apply(lambda x: re.sub(',$','', x).split(',')))




'''
关联规则简介
关联规则（Association Rules）是数据挖掘的概念，通过数据分析，
找出数据之间的关联。反映一个事物与其他事物之间的相互依存性和关联性。
电商中经常用来分析购买物品之间的相关性，如，“购买尿布的用户，很大概率购买啤酒”。
如果把 “购买尿布” 的事件记作 A，“购买啤酒” 记作事件 B，则上面规则可以写作 “A→B”。
关联规则推荐是利用关联规则实施推荐，希望达到 “将尿布放入购物篮后，
再推荐啤酒” 比 “直接推荐啤酒” 获得更好的售卖效果。（有些场景比直接推荐更有效）
'''

# 第一个参数为放入要处理的数据,
# min_support为最小支持度，商品越多同时购买的概率就越小
# min_confidence为最小置信度
# min_lift为最小提升度
model = list(apriori(res, min_support=0.02, min_confidence=0.35, min_lift= 1))
# 去除组，留下商品->商品的直接关联，再加上支持度，置信度，提升度数据支持
# join函数用逗号将列表元素连接转换成字符串类型，round依旧是四舍五入
"""
for a in model:
     print(','.join(list(a.ordered_statistics[0].items_base)),
          ' -->', list(a.ordered_statistics[0].items_add),
          '\n支持度：', round(a.support,2),
          '置信度：' , round(a.ordered_statistics[0].confidence,2),
          '提升度：' , round(a.ordered_statistics[0].lift,2))
"""

# 排序功能
new_model = []
for a in model:
    # 提取前置商品、后置商品
    base = ','.join(list(a.ordered_statistics[0].items_base))
    add = list(a.ordered_statistics[0].items_add)
    # 提取支持度、置信度、提升度（保留两位小数）
    support = round(a.support, 2)
    confidence = round(a.ordered_statistics[0].confidence, 2)
    lift = round(a.ordered_statistics[0].lift, 2)
    # 将规则信息存入字典，追加到new_model
    new_model.append({
        'base': base,
        'add': add,
        'support': support,
        'confidence': confidence,
        'lift': lift
    })

# 按提升度（lift）降序排序。key参数告诉排序函数 “用列表中每个元素的哪个属性 / 值来作为排序依据。
sorted_model = sorted(new_model, key=lambda x: x['lift'], reverse=True)

# 打印排序后的结果
for item in sorted_model:
    print(f"{item['base']} --> {item['add']}")
    print(f"支持度：{item['support']} 置信度：{item['confidence']} 提升度：{item['lift']}")
    print("-" * 40)  # 分隔线，增强可读性




'''
第二步：模型分析
输出结果分析，顾客购买酸奶和其他蔬菜的时候会同时购买全脂牛奶，
其置信度最大达到 51.29%。其他蔬菜、根茎类蔬菜和全脂牛奶同时购买的概率较高。

从购物者角度进行分析：现代生活中，大多数购物者为家庭煮妇，购买的商品大部分是食品，
随着生活质量和健康意识的增加，其他蔬菜、根茎类蔬菜和全脂牛奶均为现代家庭每日饮食所需品，
因此，其他蔬菜、根茎类蔬菜和全脂牛奶同时购买的概率较高符合现代人们的生活健康意识。

第三步：模型应用
模型结果表明顾客购买商品的时候会同时购买全脂牛奶。因此，
商场应该根据实际情况将全脂牛奶放在顾客购买商品的必经之路，或者商场显眼位置，
方便顾客拿取。其他蔬菜、根茎类蔬菜、酸奶油、猪肉、黄油、本地蛋类和多种水果同时购买的概率较高，
可以考虑捆绑销售，或者适当调整商场布置，将这些商品的距离尽量拉近，提升购物体验。
'''