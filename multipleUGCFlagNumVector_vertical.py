# -*- coding: utf-8 -*-
# 可能存在某条评论中没有某种词性单词的情况
# 统计每条UGC中不同词性单词的个数，本程序统计17类主要的词性

import re
import jieba.posseg as pseg
_author_ = 'xuyong'

in_data = open(r'comments/UGC_01.txt', 'r', encoding='UTF-8')   # 原始UGC
out_data = open(r'comments/UGC_01_fc.txt', 'w', encoding='UTF-8')   # 分词后的UGC
for line in in_data.readlines():
    line = ''.join(line)
    line = re.sub(r'[^\w\s]', '', line)
    line = line.strip()
    words = pseg.lcut(line)
    words = list(filter(None, words))
    for word, flag in words:
        out_data.write(str(flag) + "  ")
    out_data.write('\n')
in_data.close()
out_data.close()
in_data = open(r'comments/UGC_01_fc.txt', 'r', encoding='UTF-8')
comment = list(in_data)   # 列表对象，每个元素是字符串类型对象、表示in_data对象中的每行数据
in_data.close()
n_count = []    # 名词,n_count[1]表示第一条评论中的名词数量
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
usersUGC = []
for i in comment:
    str1 = ''.join(i)
    str1 = re.sub(r'[^\w\s]', '', str1)    # 删除标点符号
    str1 = str1.strip()     # 删除换行、空格
    str1 = str1.split(' ')
    str1 = list(filter(None, str1))
    if str1:
        usersUGC.append(str1)   # 得到想要的分词结果。
print("lenofusersUgc:", len(usersUGC))


for single_UGC_cx in usersUGC:
    i = 0
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
    # 统计每条评论记录中每种词性单词的数量
    for cx in single_UGC_cx:
        if cx == 'n' or cx == 'nr' or cx == 'nr1' or cx == 'nr2' or cx == 'vn' or cx == 'nrf' or cx == 'ns' or \
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
    n_count.append(cx_n)
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
    i += 1

print("n_count:", n_count)   # 示例每条评论中3种类型词性单词的数量
print("t_count:", t_count)
print("s_count:", s_count)
