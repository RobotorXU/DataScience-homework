# -*- coding: utf-8 -*-
# 计算多条评论UGC的情感强度值
# 单条UGC情感强度值，程度副词根据程度副词词典指定权值wi，程序副词权值用于计算情感强度,w1*w2...
# 对情感强度调整取值范围为[-5,5]


import jieba
import re
import time
_author_ = 'xuyong'

t1 = time.time()
# 1.读取情感词典和待处理文件
# 导入正向、负向情感词词典
posdict = open(r'sentimentDict/posdict.txt', 'r', encoding='UTF-8').read().split()   # r指出string是个raw string
negdict = open(r'sentimentDict/negdict.txt', 'r', encoding='UTF-8').read().split()

# 导入程度副词词典
mostdict = open(r'sentimentDict/degree-most.txt', 'r', encoding='UTF-8').read().split()             # 权值为2.0
verydict = open(r'sentimentDict/degree-very.txt', 'r', encoding='UTF-8').read().split()             # 权值为1.75
moredict = open(r'sentimentDict/degree-more.txt', 'r', encoding='UTF-8').read().split()             # 权值为1.5
ishdict = open(r'sentimentDict/degree-ish.txt', 'r', encoding='UTF-8').read().split()               # 权值为1.25
insufficientdict = open(r'sentimentDict/degree-insuff.txt', 'r', encoding='UTF-8').read().split()   # 权值为0.5
overdict = open(r'sentimentDict/degree-over.txt', 'r', encoding='UTF-8').read().split()             # 权值为0.25

# 导入否定词词典
inversedict = open(r'sentimentDict/notdict.txt', 'r').read().split()     # 权值为-1


def is_adv(word):
    # 判断是否为程度副词
    if word in mostdict or word in verydict or word in moredict or word in ishdict or word in overdict or\
            word in insufficientdict:
        return 1


def is_not(word):
    # 判断是否为否定词
    if word in inversedict:
        return 1


def weightof_adv(word, sentiment_value):
    # 根据程度副词的权重，调整情感词的情感值
    if word in mostdict:
        print("degree_most：", word)
        sentiment_value *= 2.0
    elif word in verydict:
        print("degree_very：", word)
        sentiment_value *= 1.75
    elif word in moredict:
        print("degree_more：", word)
        sentiment_value *= 1.5
    elif word in ishdict:
        print("degree_ish：", word)
        sentiment_value *= 1.25
    elif word in overdict:
        print("degree_over：", word)
        sentiment_value *= 0.5
    elif word in insufficientdict:
        print("degree_insuff：", word)
        sentiment_value *= 0.5
    return sentiment_value


def weightof_not(word, sentiment_value):
    # 根据否定词的权重，调整情感词的情感值
    if word in inversedict:
        print("degree_inver：", word)
        sentiment_value *= -1
    return sentiment_value


def normalization(pos_val, neg_val):
    return (pos_val + neg_val) * (5/2)


def qcsp_score(single_ugc):
    # 求单条评论语句的情感倾向总得分，评论语句参数为列表形式
    p = 0                     # 记录扫描到列表中的词的位置，列表的下标从0开始，所以设置为0比较好
    positive_senti_wrod = 0     # 记录前一个情感词的位置，初始值为0，初始位置未必是情感词，但是不影响情感值的计算。
    num_pos_senti_word = 0       # 记录正向情感词的个数
    num_neg_senti_word = 0       # 记录负向情感词的个数
    pos_val = 0                # 记录该句中的积极情感得分
    neg_val = 0                # 记录该句中的消极情感得分
    for word in single_ugc:    # 逐词分析，统计句子中的正向情感词和负向情感词个数、并计算总得分
        # 计算单个情感词语的情感词
        if word in posdict:  # 如果是积极情感词
            num_pos_senti_word += 1
            print("posword:", word)
            pos = 1   # 积极情感词基本得分为1
            for w in single_ugc[positive_senti_wrod: p]:
                if is_adv(w):
                    pos = weightof_adv(w, pos)
                if is_not(w):
                    pos = weightof_not(w, pos)
            # 调整单个情感词的情感值在[-2,2]范围
            if pos < 0:
                neg_val += pos
                num_pos_senti_word -= 1
                num_neg_senti_word += 1
            elif pos >= 0:
                pos_val += pos
            print("pos_val:", pos_val)
            print("pos_val, neg_val:", pos_val, neg_val)
            positive_senti_wrod = p + 1      # 记录情感词的位置变化
        elif word in negdict:  # 如果是消极情感词
            num_neg_senti_word += 1
            print("negword:", word)
            neg = -1
            num = 0
            for w in single_ugc[positive_senti_wrod: p]:
                if is_adv(w):
                    num += 1
                    neg = weightof_adv(w, neg)
                if is_not(w):
                    print(w)
                    neg = weightof_not(w, neg)
            if neg > 0:
                pos_val += neg
                num_neg_senti_word -= 1
                num_pos_senti_word += 1
            elif neg <= 0:
                neg_val += neg
            print("neg_val:", neg_val)
            print("pos_val, neg_val:", pos_val, neg_val)
            positive_senti_wrod = p + 1
        p += 1
    print("single UGC pos_val, neg_val:", pos_val, neg_val)
    result = pos_val + neg_val
    result = round(result, 3)    # 情感得分，保留3位小数
    print("single UGC qcsp_score:", result, '\n')
    return result


inData = open(r'comments/UGC_50.txt', 'r', encoding='UTF-8')   # 原始UGC
comment = inData.readlines()
inData.close()
qcsp_scores = ""
t = 0
for i in comment:
    t = t + 1
    sComment = ''.join(i)   # 将参数i转换为字符串
    sComment = re.sub(r'[^\w\s]', '', sComment)   # 删除标点符号
    sComment = sComment.strip()   # 删除换行、空格
    sComment = jieba.lcut(sComment)
    sComment = list(filter(None, sComment))
    print("第{}条评论！".format(t))
    qcsp_score0 = qcsp_score(sComment)
    qcsp_scores = qcsp_scores + str(qcsp_score0) + " "
outData = open(r'comments/UGC_50_QCSPScore.txt', 'w', encoding='UTF-8')
outData.write(qcsp_scores)
outData.close()
print("UGC_Sentiment_qcsp_score:", qcsp_scores)
t2 = time.time()
run_time = round(t2-t1, 2)
print("run_time:", run_time)
outData = open(r'comments/UGC_50_QCSPScore.txt', 'a', encoding='UTF-8')
outData.write(str(run_time))
outData.close()
