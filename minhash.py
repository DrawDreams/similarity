#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 正则包
import re
# 自然语言处理包
import jieba
import jieba.analyse
# html 包
import html
# 数据集处理包
from datasketch import MinHash


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


def minhash(x, y):
    m1, m2 = MinHash(), MinHash()

    s1 = extract_keywords(x)
    s2 = extract_keywords(y)

    for data in s1:
        m1.update(data.encode('utf8'))
    for data in s2:
        m2.update(data.encode('utf8'))

    return m1.jaccard(m2)


# 测试
if __name__ == '__main__':
    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()

        similarity = minhash(content_x, content_y)
        print('相似度: %.2f%%' % (similarity*100))
