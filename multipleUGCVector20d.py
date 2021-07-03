# -*- coding: utf-8 -*-
# 记录每条评论的时间、长度、情感值，计算每条评论分词结果中相应词性的单词数量（17维词性数量）


import re
import jieba.posseg as pseg
import numpy as np
_author_ = 'xuyong'

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


def is_adv(wowd_adv):
    # 判断是否为程度副词
    if wowd_adv in mostdict or wowd_adv in verydict or wowd_adv in moredict or wowd_adv in ishdict or wowd_adv\
            in overdict or wowd_adv in insufficientdict:
        return 1


def is_not(word_not):
    # 判断是否为否定词
    if word_not in inversedict:
        return 1


def weightof_adv(word_w, sentiment_value):
    # 根据程度副词的权重，调整情感词的情感值
    if word_w in mostdict:
        sentiment_value *= 2.0
    elif word_w in verydict:
        sentiment_value *= 1.75
    elif word_w in moredict:
        sentiment_value *= 1.5
    elif word_w in ishdict:
        sentiment_value *= 1.2
    elif word_w in overdict:
        sentiment_value *= 1.1
    elif word_w in insufficientdict:
        sentiment_value *= 0.5
    return sentiment_value


def weightof_not(word_w, sentiment_value):
    # 根据否定词的权重，调整情感词的情感值
    if word_w in inversedict:
        sentiment_value *= -1
    return sentiment_value


def normalization(pos_val, neg_val):
    # 标准化，取值范围[-5,5]
    return (pos_val + neg_val) * (5/2)


def single_ugc_senti_score(single_ugc):
    # 求单条评论语句的情感倾向总得分，评论语句参数为列表形式
    p = 0                     # 记录扫描到列表中的词的位置，列表的下标从0开始，所以设置为0比较好
    positive_senti_wrod = 0     # 记录前一个情感词的位置，初始值为0，初始位置未必是情感词，但是不影响情感值的计算。
    num_pos_senti_word = 0       # 记录正向情感词的个数
    num_neg_senti_word = 0         # 记录负向情感词的个数
    pos_val = 0                # 记录该句中的积极情感得分
    neg_val = 0                # 记录该句中的消极情感得分
    for word0 in single_ugc:    # 逐词分析，统计句子中的正向情感词和负向情感词个数、并计算总得分
        # 计算单个情感词语的情感词
        if word0 in posdict:  # 如果是积极情感词
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
        elif word0 in negdict:  # 如果是消极情感词
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
            positive_senti_wrod = i+1
        p += 1
    # 平均化：情感得分/情感词数量
    if num_pos_senti_word > 0:
        pos_val = pos_val / num_pos_senti_word
    if num_neg_senti_word > 0:
        neg_val = neg_val / num_neg_senti_word
    result = normalization(pos_val, neg_val)
    result = round(result, 3)    # 情感得分，保留3位小数
    return result


in_data = open(r'comments/UGC_01.txt', 'r', encoding='UTF-8')        # 原始UGC
out_data = open(r'comments/UGC_01_fc.txt', 'w', encoding='UTF-8')    # UGC分词后的每条UGC的词性情况
user_ugc_time = open(r'comments/UGC_01_time.txt', 'r', encoding='UTF-8')   # 原始评论时间
time = list(user_ugc_time)
user_ugc_time.close()
for line in in_data.readlines():    # 分词得到每条UGC的词性情况
    flags = ""
    str0 = pseg.lcut(line)
    for word, flag in str0:
        flags = flags + str(flag) + " "
    out_data.write(flags+'\n')
in_data.close()
out_data.close()
in_data = open(r'comments/UGC_01_fc.txt', 'r', encoding='UTF-8')
comment = list(in_data)
in_data.close()

n_count = []    # 名词
t_count = []    # 时间词
s_count = []    # 方位词、处所词
v_count = []    # 动词
a_count = []    # 形容词
r_count = []    # 代词
z_count = []    # 状态词
m_count = []    # 数词
d_count = []    # 副词
p_count = []    # 介词
c_count = []    # 连词
u_count = []    # 助词
o_count = []    # 拟声词、语气词、叹词
h_count = []    # 前、后缀
x_count = []    # 字符串
w_count = []    # 标点符号
eng_count = []    # 英文+数字

str1 = ''
usersUGC = []    # 记录每条UGC分词后的词性情况
for i in comment:
    str1 = ''.join(i)
    str1 = re.sub(r'[^\w\s]', '', str1)    # 删除标点符号
    str1 = str1.strip()     # 删除换行、空格
    str1 = str1.split(' ')
    str1 = list(filter(None, str1))
    if str1:
        usersUGC.append(str1)   # 得到想要的分词的词性结果，每条评论用一个列表元素表示，列表元素也是列表

userSingleUGCSentiment = []   # 记录每条评论的情感值
for uu in usersUGC:   # 计算每条评论的情感值
    score = single_ugc_senti_score(uu)
    userSingleUGCSentiment.append(score)

for single_UGC_cx in usersUGC:   # 统计每条评论中不同词性单词的数量
    cx_n = 0
    cx_t = 0
    cx_s = 0
    cx_v = 0
    cx_a = 0
    cx_r = 0
    cx_z = 0
    cx_m = 0
    cx_d = 0
    cx_p = 0
    cx_c = 0
    cx_u = 0
    cx_o = 0
    cx_h = 0
    cx_x = 0
    cx_w = 0
    cx_eng = 0
    for cx in single_UGC_cx:   # 统计每条评论中每种词性单词的数量
        if cx == 'n' or cx == 'nr' or cx == 'nr1' or cx == 'nr2' or cx == 'vn' or cx == 'nrf' or cx == 'ns' or\
                cx == 'nsf' or cx == 'nt' or cx == 'nz' or cx == 'nl' or cx == 'ng':
            cx_n += 1
        elif cx == 't':
            cx_t += 1
        elif cx == 's' or cx == 'f':
            cx_s += 1
        elif cx == 'v':
            cx_v += 1
        elif cx == 'a':
            cx_a += 1
        elif cx == 'r':
            cx_r += 1
        elif cx == 'z':
            cx_z += 1
        elif cx == 'm':
            cx_m += 1
        elif cx == 'd':
            cx_d += 1
        elif cx == 'p':
            cx_p += 1
        elif cx == 'c':
            cx_c += 1
        elif cx == 'u' or cx == 'ul' or cx == 'uj' or cx == 'uv' or cx == 'uz':
            cx_u += 1
        elif cx == 'o':
            cx_o += 1
        elif cx == 'h':
            cx_h += 1
        elif cx == 'x':
            cx_x += 1
        elif cx == 'w':
            cx_w += 1
        elif cx == 'eng':
            cx_eng += 1
    n_count.append(cx_n)   # 每条评论中的相应词性单词的数量
    t_count.append(cx_t)
    s_count.append(cx_s)
    v_count.append(cx_v)
    a_count.append(cx_a)
    r_count.append(cx_r)
    z_count.append(cx_z)
    m_count.append(cx_m)
    d_count.append(cx_d)
    p_count.append(cx_p)
    c_count.append(cx_c)
    u_count.append(cx_u)
    o_count.append(cx_o)
    h_count.append(cx_h)
    x_count.append(cx_x)
    w_count.append(cx_w)
    eng_count.append(cx_eng)

userUGCVsm = []    # 定义空列表，用户全部评论的20维特征（时间、长度、情感值、17类词性数量）
j = 0     # 定位评论时间
for i in usersUGC:    # 控制循环次数为UGC条数
    uu = np.zeros(20, dtype=np.int)   # 定义20维的0向量
    t = ''
    for s in time[j]:    # 去除“:”
        if s == ':':
            continue
        t += s
    uu[0] = t    # 时间
    uu[1] = len(i)    # 长度（分词数量）
    uu[2] = userSingleUGCSentiment[j]*100   # 情感值,变量是整型，乘100，使得情感值保留2位小数有效位
    uu[3] = n_count[j]
    uu[4] = t_count[j]
    uu[5] = s_count[j]
    uu[6] = v_count[j]
    uu[7] = a_count[j]
    uu[8] = r_count[j]
    uu[9] = z_count[j]
    uu[10] = m_count[j]
    uu[11] = d_count[j]
    uu[12] = p_count[j]
    uu[13] = c_count[j]
    uu[14] = u_count[j]
    uu[15] = o_count[j]
    uu[16] = h_count[j]
    uu[17] = x_count[j]
    uu[18] = w_count[j]
    uu[19] = eng_count[j]
    j += 1
    userUGCVsm.append(uu)
print(userUGCVsm[0])
out_data = open(r'comments/UGC_01_20vec.txt', 'w', encoding='UTF-8')
for v in userUGCVsm:
    print(v)
out_data.close()
