# -*- coding: utf-8 -*-
import facebook
import re
import json

def crawing(graph, cowbieNTUST_id, args):
    pattent = re.compile(u'[\U00010000-\U0010ffff]')
    nextPage = ""
    messages = []
    posts = graph.get_object(cowbieNTUST_id, **args)

    nextPage = "nextpage"
    
    while (nextPage != ""):
        for post in posts['data']:
            comments = []
            if ('message' in post):
                myMSG = re.sub(pattent, '', post['message'])
                if ('comments' in post):
                    for cmts in post['comments']['data']:
                        myCMTS = re.sub(pattent, '', cmts['message'])
                        comments.append({ 'Author': {'id':cmts['from']['id'], 'name':cmts['from']['name'] }, 'msg':myCMTS, 'like_count': cmts['like_count'], 'Time': cmts['created_time']})
                
                if ('likes' in post):
                    messages.append({'id':post['id'], 'Time':post['created_time'], 'msg':myMSG, 'likes':post['likes']['data'], 'total_likes':len(post['likes']['data']), 'comments': comments})
                else:
                    messages.append({ 'id':post['id'], 'Time':post['created_time'], 'msg':myMSG, 'likes':[] , 'total_likes':0, 'comments': comments})

        if ('paging' in posts):
            nextPage = posts['paging']['next'] 
        else:
            break

        nextPage_id = re.search('[0-9]+$', nextPage).group(0)
        print nextPage_id
        args['until'] = nextPage_id 
        posts = graph.get_object(cowbieNTUST_id, **args)
    return messages

if __name__ == "__main__":
    out = open('hateNTUST.txt', 'w')
    cowbeiList = []
    TOKEN = 'CAACEdEose0cBAER5blWimWBe2L7UJQLEvsFdQEwKur3icwQUB8OhCa60v63wnwa3rrHGBOK4ZBCSmiewE2IjYRKAJFIZAMKCTbJpVC9N5QF7gzL4exvo2n1QA1px7Nuli3yTymIos74A7dJa9TwR60sBWXE5gTBZCLZA7KZC2fbg2oD1UL6RRUNNEMSdCP6cZD'
    graph = facebook.GraphAPI(TOKEN)
      
    cowbieNTUST_id = '671080219594594/posts';

    args = {'fields' : 'id,message,likes,comments', 'limit' : 200, 'until' : ''}
    
    messages = crawing(graph, cowbieNTUST_id, args)
    out.write(json.dumps(messages, ensure_ascii=False, indent=2).encode("utf8"))