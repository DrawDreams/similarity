#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 正则
import re
# html 包
import html
# 数学包
import math
# 自然语言处理包
import jieba
import jieba.analyse


class SimHash(object):

    def getBinStr(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            return str(x)

    def simHash(self, content):
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?<\/style>)|(<[^>]+>)',re.S)
        content = re_exp.sub(' ',content)
        # html 转义符实体化
        content = html.unescape(content)
        seg = jieba.cut(content.lower(), cut_all=True)
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=True)

        ret = []
        for keyword, weight in keywords:
            binstr = self.getBinStr(keyword)
            keylist = []
            for c in binstr:
                weight = math.ceil(weight)
                if c == "1":
                    keylist.append(int(weight))
                else:
                    keylist.append(-int(weight))
            ret.append(keylist)
        # 对列表进行"降维"
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)

    def getDistince(self, simhash1, simhash2):
        length = 0
        for index, char in enumerate(simhash1):
            if char == simhash2[index]:
                continue
            else:
                length += 1
        return length


# 测试
if __name__ == '__main__':
    simhash = SimHash()

    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()

        simhash1 = simhash.simHash(content_x)
        simhash2 = simhash.simHash(content_y)

        distince = simhash.getDistince(simhash1, simhash2)
        threshold = 3
        print(f'相似哈希指纹1: {simhash1}\n相似哈希指纹2: {simhash2}')
        print(f'海明距离：{distince} 判定距离：{threshold} 是否相似：{distince <= threshold}')
