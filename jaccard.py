#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 正则包
import re
# 自然语言处理包
import jieba
import jieba.analyse
# html 包
import html


def extract_keywords(content):
    # 正则过滤 html 标签
    re_exp = re.compile(r'<[^>]+>',re.S)
    content = re_exp.sub(' ', content)
    # html 转义符实体化
    content = html.unescape(content)
    # 内容切割
    seg = jieba.cut(content.lower(), cut_all=True)
    # 关键词提取
    keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
    return keywords


def jaccard(x, y):
    # 去除停用词
    jieba.analyse.set_stop_words('./files/stopwords.txt')

    # 分词与关键词提取
    keywords_x = extract_keywords(x)
    keywords_y = extract_keywords(y)

    # jaccard相似度计算
    intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
    union = len(list(set(keywords_x).union(set(keywords_y))))
    # 除零处理
    similarity = float(intersection)/union if union != 0 else 0
    return similarity


# 测试
if __name__ == '__main__':
    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()
        similarity = jaccard(content_x, content_y)
        print('相似度: %.2f%%' % (similarity*100))
