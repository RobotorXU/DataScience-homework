# -*- coding: utf-8 -*-
# 计算文本型UGC句子情感强度：正向、负向情感词数量和


import jieba
import re
import time

# 程序运行开始时间
t1 = time.time()
# 1.读取情感词典和待处理文件
# 导入正向、负向情感词词典
posdict = open(r'sentimentDict/posdict.txt', 'r', encoding='UTF-8').read().split()   # r告诉编译器这个string是个raw string
negdict = open(r'sentimentDict/negdict.txt', 'r', encoding='UTF-8').read().split()

# 函数，求单条语句评论UGC的情感倾向总得分，参数为列表形式的单条语句UGC


def sp_score(single_ugc):
    num_pos_senti_word = 0       # 记录正向情感词的个数
    num_neg_senti_word = 0       # 记录负向情感词的个数
    sps = 0    # 记录正向、负向情感词数量和，每个正向情感词记为+1、每个负向情感词记为-1
    for word in single_ugc:   # 逐词分析，统计句子中的正向情感词和负向情感词个数、并计算总得分
        if word in posdict:   # 如果是正向情感词
            print("posword:", word)
            num_pos_senti_word += 1
            sps += 1
        elif word in negdict:  # 如果是负向情感词
            print("negword:", word)
            num_neg_senti_word += 1
            sps -= 1
    print("num_pos_senti_word:", num_pos_senti_word, "num_neg_senti_word:", num_neg_senti_word)
    print("single UGC sp_score:", sps, '\n')
    return sps


# singleComment = ['快递', '收到', '了', '外观', '挺', '好看', '使用', '了', '一会儿', '运行', '速度',
# '很', '流畅', '物流', '服务', '都', '很', '不错', '总体', '很', '满意']
inData = open(r'comments/UGC_50.txt', 'r', encoding='UTF-8')   # 原始UGC
comment = inData.readlines()    # 按行读入原始数据
inData.close()
SPScores = ""    # 记录所有UGC的总评分
t = 0    # 记录第几条UGC
for i in comment:
    t = t + 1
    sComment = ''.join(i)   # 将参数i转换为字符串
    sComment = re.sub(r'[^\w\s]', '', sComment)   # 删除标点符号
    sComment = sComment.strip()   # 删除换行、空格
    sComment = jieba.lcut(sComment)
    sComment = list(filter(None, sComment))    # 剔除序列中的False值，如空字符串、False、[]、None、{}、()等
    print("第{}条评论！".format(t))
    SPScores0 = sp_score(sComment)
    SPScores = SPScores + str(SPScores0) + " "
outData = open(r'comments/UGC_50_SPScore.txt', 'w', encoding='UTF-8')
outData.write(SPScores)
outData.close()
print("UGC_Sentiment_SPScore:", SPScores)
t2 = time.time()
run_time = round(t2-t1, 2)
print("run_time:", run_time)
outData = open(r'comments/UGC_50_SPScore.txt', 'a', encoding='UTF-8')
outData.write(str(run_time))    # 执行时间写入文件
outData.close()
