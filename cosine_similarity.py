#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 正则包
import re
# html 包
import html
# 自然语言处理包
import jieba
import jieba.analyse
# 机器学习包
from sklearn.metrics.pairwise import cosine_similarity


def exractKeyword(content):
    # 正则过滤 html 标签
    re_exp = re.compile(r'(<style>.*?<\/style>)|(<[^>]+>)',re.S)
    content = re_exp.sub(' ',content)
    # html 转义符实体化
    content = html.unescape(content)
    # 切割
    seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
    # 提取关键词
    keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
    return keywords


def oneHot(word_dict, keywords):
    cut_code = [word_dict[word] for word in keywords]
    cut_code = [0]*len(word_dict)
    for word in keywords:
        cut_code[word_dict[word]] += 1
    return cut_code


def cosineSimilarity(s1, s2):
    # 提取关键词
    keywords1 = exractKeyword(s1)
    keywords2 = exractKeyword(s2)
    # 词的并集
    union = set(keywords1).union(set(keywords2))
    # 编码
    word_dict = {}
    i = 0
    for word in union:
        word_dict[word] = i
        i += 1
    # oneHot编码
    s1_cut_code = oneHot(word_dict, keywords1)
    s2_cut_code = oneHot(word_dict, keywords2)
    # 余弦相似度计算
    sample = [s1_cut_code, s2_cut_code]
    # 除零处理
    try:
        sim = cosine_similarity(sample)
        return sim[1][0]
    except:
        return 0.0


# 测试
if __name__ == '__main__':
    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()
        similarity = cosineSimilarity(content_x, content_y)
        print('相似度: %.2f%%' % (similarity*100))
