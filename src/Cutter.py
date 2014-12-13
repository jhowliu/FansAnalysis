# -*- coding: utf-8 -*- 
import jieba.posseg as pseg
import jieba
import json
import math
import sys

jieba.load_userdict('../data/dict.txt')

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
        ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
        々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
        ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…/''')

def loadJson(fileName):
    tmp = open(fileName)
    posts = json.load(tmp)
    tmp.close()
    return posts

def writeResult(fileName, result):
    out = open(fileName, 'w')

    for w in result:
        out.write(w.encode('utf8')+'\n')
    out.close()


def cutter(data, num):
    VSM = []
    keywords = {}

    for post in data:
        tmp = {}
        if 'msg' in post:
            # Filter punctuation 
            s = post['msg']
            s = filter(lambda x: x not in punct, s)

            segs = pseg.cut(s)

            for seg in segs:
                hased = False
                if seg.flag == 'n' or seg.flag == 'ns':
                    if seg.word not in keywords and not hased:
                        keywords[seg.word] = 1
                    else:
                        keywords[seg.word] += 1

                    hashed = True

                    if seg.word not in tmp:
                        tmp[seg.word] = 1
                    else:
                        tmp[seg.word] += 1

        VSM.append([tmp])

    candidateSet, candidates = takeCandidate(VSM, keywords, num)

    return list(set(candidateSet)), candidates

# Reture the top "num" term
def calculateTF(term):
    termOfSum = sum(term.values())

    TF = [(y, float(x)/float(termOfSum)) for x, y in zip(term.values(), term.keys())]

    TF = filter(lambda x: x[0].find('http') == -1, TF)
    TF = filter(lambda x:x[0].isdigit() != True, TF)
    TF = filter(lambda x: len(x[0]) > 1, TF)
    TF = sorted(TF, key=lambda x: x[1])

    TF.reverse()

    return TF

def calculateIDF(terms, keywords, length):
    idfList = map(lambda x: (x[0], math.log(float(length)/float(keywords[x[0]])), 10), terms)

    return idfList

def takeCandidate(VSM, keywords, num):
    candidates = []
    candidateSet = []

    for x in VSM:
        tf = calculateTF(x[0])
        idf = calculateIDF(tf, keywords, len(VSM))
        tmp = map(lambda x, y: (x[0], x[1]*y[1]), tf, idf)
        tmp = sorted(tmp, key=lambda x: x[1])
        tmp = map(lambda x: x[0], tmp)
        tmp.reverse()
        candidates.append(tmp[:num])
        candidateSet.extend(tmp[:num])

    return candidateSet, candidates

def filterDataset(data):
    data = sorted(data.items(), key=lambda x:x[1])
    data.reverse()

    data = filter(lambda x: len(x[0]) > 1, data)
    data = filter(lambda x: x[0].find('http') == -1, data)

    return data

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python Cutter.py <fileName> <Number>"
        exit(1)

    posts = loadJson(sys.argv[1])
    candidates, candidateSet = cutter(posts, int(sys.argv[2]))

    #for candidates in candidateSet:
    #    for candidate in candidates:
    #        print candidate
    #    print

    writeResult(sys.argv[1].replace('.json', '.txt'), candidates)

    print len(candidates), len(candidateSet)
