import sys
import json

def get_data(name):
    print name
    tmp = open(name + '.json')
    data = json.load(tmp)
    return data

def processing(data):
    likeCollection = []

    for post in data:
        likeCollection.append({post['id']:post['like_count']})
    
    return likeCollection

def Run(inputfile, output):
    data = get_data(inputfile)
    out = open(output + '.csv', 'w')
    collection = processing(data)
    json.dump(collection, out, indent=4)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Useage: <Input json> <output name>'
    else:
        Run(sys.argv[1], sys.argv[2])

