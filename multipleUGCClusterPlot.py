# -*- coding: utf-8 -*-

# 用TSNE进行数据降维并展示聚类结果
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

tsne = TSNE()
tsne.fit_transform(data) #进行数据降维,并返回结果
tsne = pd.DataFrame(tsne.embedding_, index = data.index) #转换数据格式

plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

# 不同类别用不同颜色和样式绘图
d = tsne[r[u'聚类类别'] == 0]     # 找出聚类类别为0的数据对应的降维结果
plt.plot(d[0], d[1], 'r.')
d = tsne[r[u'聚类类别'] == 1]
plt.plot(d[0], d[1], 'go')
d = tsne[r[u'聚类类别'] == 2]
plt.plot(d[0], d[1], 'b*')
d = tsne[r[u'聚类类别'] == 3]
plt.plot(d[0], d[1], 'b*')
d = tsne[r[u'聚类类别'] == 4]
plt.plot(d[0], d[1], 'b*')
plt.show()
