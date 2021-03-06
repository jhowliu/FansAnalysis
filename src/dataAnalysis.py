import sys
import numpy as np

def loadFileToDict(fileName):
    tmp = open(fileName)
    userDict = {}
    label = []
    for line in tmp.readlines():
        data = line.replace('\r\n', '').split(',')
        if data[0] == 'uid':
            label = data[1:len(data)]
        else:
            userDict[data[0]] = map(lambda x: int(x), data[1:len(data)])

    return userDict, label

def loadClusteringResult(fileName):
    tmp = open(fileName)
    result = []

    for line in tmp.readlines():
        result.append(line.replace('\n', '').split(','))

    return result

# Return postid respectively
def filterPK(label):
    label = np.array(label)

    pig = filter(lambda x: x.find('652438848137404') == 0, label)
    kp  = filter(lambda x: x.find('136845026417486') == 0, label)

    return pig, kp

def getClusterPost(result, user, label, threshold):
    data = []
    label = np.array(label)
    for t in result:
        tmp = []
        for uid in t[1:len(t)]:
            tmp.append(user[uid])

        tmp = np.array(tmp)
        # 0 is sum of column
        tmp = label[np.sum(tmp, 0) > threshold]

        data.append(tmp.tolist())

    return data

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python dataAnalysis.py <UserMatrix> <ClusteringResult>"
        sys.exit(1)

    user, label = loadFileToDict(sys.argv[1])
    result = loadClusteringResult(sys.argv[2])
