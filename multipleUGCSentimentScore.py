# -*- coding: utf-8 -*-
# 算多条评论UGC的情感强度值
# 单条UGC情感强度值，程度副词根据程度副词词典指定权值wi，程序副词权值用于计算情感强度：w1*w2...，求n次方根
# 对情感强度调整取值范围为[-5,5]

import jieba
import re
_author_ = 'xuyong'

# 1.读取情感词典和待处理文件
# 导入正向、负向情感词词典
posdict = open(r'sentimentDict/posdict.txt', 'r', encoding='UTF-8').read().split()   # r指明string是个raw string
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
        sentiment_value *= 2.0
    elif word in verydict:
        sentiment_value *= 1.75
    elif word in moredict:
        sentiment_value *= 1.5
    elif word in ishdict:
        sentiment_value *= 1.25
    elif word in insufficientdict:
        sentiment_value *= 0.5
    elif word in overdict:
        sentiment_value *= 0.25
    return sentiment_value


def weightof_not(word, sentiment_value):
    # 根据否定词的权重，调整情感词的情感值
    if word in inversedict:
        sentiment_value *= -1
    return sentiment_value


def normalization(pos_val, neg_val):
    # 标准化，取值范围[-5,5]
    return (pos_val + neg_val) * (5/2)


def single_ugc_senti_score(single_ugc):    # 单条UGC情感值计算函数，可改进！！！
    # 求单条评论语句的情感倾向总得分，评论语句参数为列表形式
    p = 0                     # 记录扫描到列表中的词的位置，列表的下标从0开始，所以设置为0比较好
    positive_senti_wrod = 0     # 记录前一个情感词的位置，初始值为0，初始位置未必是情感词，但是不影响情感值的计算。
    num_pos_senti_word = 0       # 记录正向情感词的个数
    num_neg_senti_word = 0         # 记录负向情感词的个数
    pos_val = 0                # 记录该句中的积极情感得分
    neg_val = 0                # 记录该句中的消极情感得分
    for word in single_ugc:    # 逐词分析，统计句子中的正向情感词和负向情感词个数、并计算总得分
        # 计算单个情感词语的情感词
        if word in posdict:  # 如果是积极情感词
            num_pos_senti_word += 1
            pos = 1   # 积极情感词基本得分为1
            # 根据前面的所有副词、否定词，调整当前情感词的情感值，统计前一个情感词开始到当前情感词之间的所有副词数量
            num = 0  # 统计副词个数
            for w in single_ugc[positive_senti_wrod: p]:
                if is_adv(w):
                    num += 1
                    pos = weightof_adv(w, pos)
                if is_not(w):
                    pos = weightof_not(w, pos)
            # 调整单个情感词的情感值在[-2,2]范围
            if num > 1:
                if pos >= 0:
                    pos = pow(pos, 1 / num)
                else:
                    pos = (-1)*pow(abs(pos), 1/num)
            pos_val += pos
            positive_senti_wrod = p + 1      # 记录情感词的位置变化
        elif word in negdict:  # 如果是消极情感词
            num_neg_senti_word += 1
            neg = -1
            num = 0
            for w in single_ugc[positive_senti_wrod: p]:
                if is_adv(w):
                    num += 1
                    neg = weightof_adv(w, neg)
                if is_not(w):
                    neg = weightof_not(w, neg)
            if num > 1:
                if neg >= 0:
                    neg = pow(neg, 1/num)
                else:
                    neg = (-1)*pow(abs(neg), 1/num)
            neg_val += neg
            positive_senti_wrod = p + 1
        p += 1
    # 平均化：情感得分/情感词数量
    if num_pos_senti_word > 0:
        pos_val = pos_val/num_pos_senti_word
    if num_neg_senti_word > 0:
        neg_val = neg_val/num_neg_senti_word
    result = normalization(pos_val, neg_val)
    result = round(result, 3)    # 情感得分，保留3位小数
    return result


in_data = open(r'comments/UGC_01.txt', 'r', encoding='UTF-8')   # 原始UGC
comment = in_data.readlines()
in_data.close()
multipleCommentsScore = ""
for i in comment:
    sComment = ''.join(i)   # 将参数i转换为字符串
    sComment = re.sub(r'[^\w\s]', '', sComment)   # 删除标点符号
    sComment = sComment.strip()   # 删除换行、空格
    sComment = jieba.lcut(sComment)
    sComment = list(filter(None, sComment))
    singleCommentScore = single_ugc_senti_score(sComment)
    multipleCommentsScore = multipleCommentsScore + str(singleCommentScore) + " "
out_data = open(r'comments/UGC_01_Score.txt', 'w', encoding='UTF-8')
out_data.write(multipleCommentsScore)
print(multipleCommentsScore)
