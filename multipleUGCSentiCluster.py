# -*- coding: utf-8 -*-
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.manifold import TSNE
# from sklearn.cluster import KMeans
# import scipy
# import scipy.cluster.hierarchy as sch
# import matplotlib.pylab as plt


import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
import multipleUGCVector20d

# np数据从0开始计算，第0维维序号排除，第10维为标签排除，所以为1到9

# k-means聚类
# 将原始数据做归一化（白化）处理
data_01 = whiten(multipleUGCVector20d.userUGCVsm)    # ：先求各数组标准差，然后将数组每个元素分别除以该标准差
weight = [0.25, 0.25, 0.25, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015,
          0.015, 0.015, 0.015, 0.015, 0.015, 0.010]
data = data_01 * weight

# k-means最后输出的结果其实是两维的,第一维是聚类中心,第二维是损失distortion,我们在这里只取第一维,所以最后有个[0]
# centroid = kmeans(data,max(cluster))[0]
centroid = kmeans(data, 5)[0]    # 5个聚类中心，每个中心是一个20维向量
distortion = kmeans(data, 5)[1]    # 聚类损失值，1个
print("begin for centroid:")
print(centroid)
print("begin for distortion:")
print(distortion)
# 使用vq函数根据聚类中心对所有数据进行分类,vq的输出也是两维的,[0]表示的是所有数据的label
label = vq(data, centroid)[0]
num = np.zeros(5, dtype=np.int)
for i in label:
    if i == 0:
        num[0] += 1
    elif i == 1:
        num[1] += 1
    elif i == 2:
        num[2] += 1
    elif i == 3:
        num[3] += 1
    elif i == 4:
        num[4] += 1 
print('num =', num)
print("Final clustering by k-means:\n", label)

file = open(r'comments/UGC_01_cluster_result.txt', mode='w')
file.write("Final clustering by k-means:\n")        # 将空格写入txt文件中
file.write(str(label))
file.write('\n')      # 将回车写入txt文件中

file.write('diff_cluster_center =')
file.write(str(centroid))
file.write('\n') 

file.write('diff_cluster_num =')
file.write(str(num))
file.write('\n') 

file.write('distortion=')
file.write(str(distortion))

file.close()
