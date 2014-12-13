import sys
import numpy

def loadFileToDict(fileName):
    tmp = open(fileName)
    userDict = {}
    label = []
    for line in tmp.readlines():
        data = line.replace('\r\n', '').split(',')
        if data[0] == 'uid':
            label = data[1:len(data)-1]
        else:
            userDict[data[0]] = map(lambda x: int(x), data[1:len(data)-1])

    return userDict, label

def loadClusteringResult(fileName):
    tmp = open(fileName)
    result = []

    for line in tmp.readlines():
        result.append(line.replace('\n', '').split(','))
    
    return result

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python dataAnalysis.py <UserMatrix> <ClusteringResult>"
        sys.exit(1)
    
    user, label = loadFileToDict(sys.argv[1])
    result = loadClusteringResult(sys.argv[2])
