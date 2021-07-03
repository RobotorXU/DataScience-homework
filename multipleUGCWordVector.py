# -*- coding: utf-8 -*-
# 生成每条评论UGC中的分词向量，每条评论单词写入文件中的一行，函数返回列表形式的分词结果、每个元素也是列表形式


import re
import jieba.posseg as pseg


def word_vector(f1, f2):
    in_data = open(f1, 'r', encoding='UTF-8')        # 原始UGC
    out_data = open(f2, 'w', encoding='UTF-8')    # 分词后的UGC
    for line in in_data.readlines():
        words = ""
        str0 = pseg.lcut(line)
        for word, flag in str0:
            words = words + str(word) + " "
        out_data.write(words)
    in_data.close()
    out_data.close()
    in_data = open(f2, 'r', encoding='UTF-8')
    comment = list(in_data)
    in_data.close()
    users_ugc_word_vector = []
    out_data = open(f2, 'w', encoding='UTF-8')
    for i in comment:
        str1 = ''.join(i)
        # print("1:",type(str1),str1)
        str1 = re.sub(r'[^\w\s]', '', str1)  # 删除标点符号
        str1 = str1.strip()  # 删除换行、空格
        str1 = str1.split(' ')
        # print("2:",type(str1),str1)
        str1 = list(filter(None, str1))
        if str1:
            users_ugc_word_vector.append(str1)  # 得到想要的分词结果。
            out_data.write(''.join(str1) + '\n')   # 写入文件必须是字符串
    out_data.close()
    return users_ugc_word_vector   # 返回列表格式的UGCs


fread = r"comments/UGC_01.txt"
fwrite = r"comments/UGC_01_WV.txt"
userLst = word_vector(fread, fwrite)
print(type(userLst), type(userLst[0]), len(userLst))
for l in userLst:
    print(l)
#预处理阶段完成
singleUGC = [['快递','收到','了','外观','挺','好看','的','使用','了','一会儿','运行','速度','也','很','流畅','物流', ………… ]]