import numpy as np
import json
import sys

def readfile(fileName):
    tmp = open(fileName+'.json')
    data = json.load(tmp)

    return data

def getLabel(data):
    label = np.array([0 for _ in range(len(data))])

    return label

def createMatrix(data, label):
    userLikes = {}

    for i in range(0, len(data)):
        for x in data[i]['likes']:
            if x['uid'] in userLikes:
                userLikes[x['uid']].append(i)
            else:
                userLikes[x['uid']] = [i]

    matrix = []

    for x in userLikes:
        tmp = [0 for _ in range(len(data))]
        for index in userLikes[x]:
            tmp[index] = 1
        matrix.append(tmp)

    return matrix, userLikes

if __name__ == '__main__':
    tmp = []

    if len(sys.argv) >= 2:
        for x in sys.argv[1:]:
            tmp.append(x)
    for x in tmp:
        data = readfile(x)
        label = getLabel(data[0])
        matrix, userLikes = createMatrix(data, label)

        out = open(x + '.csv', 'w')
        id_out = open(x + '_id.csv', 'w')

        for x in matrix:
            out.write(','.join(str(a) for a in x) + '\n')
        for x in userLikes:
            id_out.write(str(x) + '\n')

        id_out.close()
        out.close()



