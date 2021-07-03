# -*- coding: utf-8 -*-
# 生成评论的词性向量，每条评论单词的词性写入文件中的一行，函数返回列表形式的单词词性结果、每个元素也是列表形式

import re
import jieba.posseg as pseg


def flag_vector(f1, f2):
    in_data = open(f1, 'r', encoding='UTF-8')        # 原始UGC
    out_data = open(f2, 'w', encoding='UTF-8')    # 分词后的UGC
    for line in in_data.readlines():
        flags = ""
        str0 = pseg.lcut(line)
        for word, flag in str0:
            flags = flags + str(flag) + " "
        out_data.write(flags + '\n')
    in_data.close()
    out_data.close()
    in_data = open(f2, 'r', encoding='UTF-8')
    comment = list(in_data)
    in_data.close()
    users_ugc_flag_vector = []
    out_data = open(f2, 'w', encoding='UTF-8')
    for i in comment:
        str1 = ''.join(i)
        str1 = re.sub(r'[^\w\s]', '', str1)  # 删除标点符号
        str1 = str1.strip()  # 删除换行、空格
        str1 = str1.split(' ')
        # print("2:",type(str1), str1)
        str1 = list(filter(None, str1))
        if str1:
            users_ugc_flag_vector.append(str1)  # 得到想要的分词结果。
            out_data.write(''.join(str1) + '\n')   # 写入文件必须是字符串
    out_data.close()
    return users_ugc_flag_vector   # 返回列表格式的UGCs


fread = r"comments/UGC_01.txt"
fwrite = r"comments/UGC_01_FV.txt"
userLst = flag_vector(fread, fwrite)
print(type(userLst), type(userLst[0]), len(userLst))
for f in userLst:
    print(f)
