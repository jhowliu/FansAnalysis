# -*- coding: utf-8 -*-

import jieba
import json
import sys

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
        ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
        々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
        ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

def loadJson(fileName):
    tmp = open(fileName)
    posts = json.load(tmp)

    return posts

def cutter(data):
    for post in data:
        if 'msg' in post:
            # Filter punctuation 
            s = post['msg']
            s = filter(lambda x: x not in punct, s)
            print s
            print 
            #segs = jieba.cut(s)
            #for seg in segs:
            #    print seg


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "python Cutter.py <fileName>"

    posts = loadJson(sys.argv[1])
    cutter(posts)

