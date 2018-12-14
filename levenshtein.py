#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

# 编辑距离包
import Levenshtein


# 测试
if __name__ == '__main__':
    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()
        distance = Levenshtein.distance(content_x, content_y)
        print(f'编辑距离为: {distance}')
