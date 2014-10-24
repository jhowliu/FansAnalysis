import operator
import json
import sys

def countLikes(data, output):
    total = {}

    for i in range(len(data)):
        for j in range(len(data[i]['likes'])):
            if total.has_key(data[i]['likes'][j]['uid']):
                total[data[i]['likes'][j]['uid']] += 1
            else:
                total[data[i]['likes'][j]['uid']] = 1

    sorted_total = sorted(total.items(), key = operator.itemgetter(1), reverse = 1)
    sorted_num = sorted(total.values(), reverse = 1)

    out = open(output + '.csv', 'w')
    out_num = open(output + '_noid.csv', 'w')
    
    print sorted_num[0]
    out_num.write(','.join(str(x) for x in sorted_num)) 

    out_num.close()
    out.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
       print "Usage: <JsonFile> <OutputName>"
       exit(-1)
    filename = sys.argv[1]
    output = sys.argv[2]
    raw_data = open(filename,'r')
    data = json.load(raw_data)

    countLikes(data, output)
