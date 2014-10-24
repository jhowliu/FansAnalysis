import operator
import json
import sys

def countLikes(data, output):
    total = {}
    
    for post in data:
        for like in post['likes']:
            if like['uid'] in total:
                total[like['uid']] += 1
            else:
                total[like['uid']] = 1
    
    sorted_total = sorted(total.items(), key = operator.itemgetter(1), reverse = 1)
    sorted_num = sorted(total.values(), reverse = 1)
    
    likes = {}  
    # Transfer tuple to dict
    for key, value in sorted_total:
        likes[key] = value

    out_id = open(output + '_id.csv', 'w')
    out_num = open(output + '_noid.csv', 'w')

    out_id.write(','.join(str(x) for x in likes))
    out_num.write(','.join(str(x) for x in sorted_num)) 

    out_num.close()
    out_id.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
       print "Usage: <JsonFile> <OutputName>"
       exit(-1)
    filename = sys.argv[1]
    output = sys.argv[2]
    raw_data = open(filename,'r')
    data = json.load(raw_data)

    countLikes(data, output)
