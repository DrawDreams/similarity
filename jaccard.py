# -*- coding:utf-8 -*-

# 正则包
import re
# 自然语言处理包
import jieba
import jieba.analyse
# 转义字符实体化的包,py2-3兼容
try:
    # for py3
    import html
except:
    # for py2
    import HTMLParser
    html = HTMLParser.HTMLParser()


def extract_keywords(content):
    # 正则过滤 html 标签
    re_exp = re.compile(r'<[^>]+>',re.S)
    content_html = re_exp.sub(' ',content)
    # html 转义符实体化
    content = html.unescape(content_html)
    # 内容切割
    seg = jieba.cut(content, cut_all=True)
    # 关键词提取
    keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
    return keywords


def jaccard(x,y):
    # 去除停用词
    jieba.analyse.set_stop_words('./stopwords.txt')

    # 分词与关键词提取
    keywords_x = extract_keywords(x)
    keywords_y = extract_keywords(y)

    # jaccard相似度计算
    intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
    union= len(list(set(keywords_x).union(set(keywords_y))))
    # 除零处理
    similarity = float(intersection)/float(union) if union != 0 else 0
    # 返回值 （1.相似度 2.第一个内容有意义的词的个数 3.第二个内容有意义的词的个数
    return similarity,len(keywords_x),len(keywords_y)


# 测试
if __name__ == '__main__':
    content_one = '<span style="font-size: 16px; font-family: arial, helvetica, sans-serif;">2,&nbsp;Elastic cuffs and stretch fabric provide snug-fitting fte dwadw ddawd and games.</span>'
    content_two = '<span style="font-size: 16px; font-family: arial, helvetica, sans-serif;">2,&nbsp;Elastic cuffs and stretch fabric provide snug-fitting fte dwadw ddawd and test.</span>'
    similarity, len_one, len_two = jaccard(content_one, content_two)
    print(similarity,len_one,len_two)
