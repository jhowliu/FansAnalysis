# -*- coding: utf-8 -*-
import facebook
import re
import json

def crawing(graph, Fans_id, args):
    pattent = re.compile(u'[\U00010000-\U0010ffff]')
    nextPage = ""
    messages = []
    posts = graph.get_object(Fans_id, **args)

    nextPage = "nextpage"
    
    while (nextPage != ""):
        for post in posts['data']:
            comments = []
            if ('message' in post):
                myMSG = re.sub(pattent, '', post['message'])
                if ('comments' in post):
                    for cmts in post['comments']['data']:
                        myCMTS = re.sub(pattent, '', cmts['message'])
                        comments.append({ 'id':cmts['id'] ,'Author': {'id':cmts['from']['id'], 'name':cmts['from']['name'] }, 'msg':myCMTS, 'like_count': cmts['like_count'], 'Time': cmts['created_time']})
                
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
        posts = graph.get_object(Fans_id, **args)
    return messages

if __name__ == "__main__":
    out = open('Fans.txt', 'w')
    
    TOKEN = "CAACEdEose0cBAMGSWnJO92WreoNyooZAE5APuc94DJzjMKjtqLE9qqXLLuMuTCx8lLZAlU8dvukZAbqTopvwd6ni2mZBglo0FeIe6oT6cZCZAZAqFnKdlMMvyxlCl68ZAri2ajAhqP9M8pfrcLDJgQYTabIN8rh0YLiyM2k4C9RqWovj9MGaqcZAdteX6Uh6sV07vbIjDFMZAoyDbDcNudZB0tOfPLGkv61F5cZD"

    graph = facebook.GraphAPI(TOKEN)
      
    Fans_id = '544241848968882/posts';
    
    args = {'fields' : 'id, message, likes, comments', 'limit' : 20, 'until' : ''}
    
    messages = crawing(graph, Fans_id, args)

    out.write(json.dumps(messages, ensure_ascii=False, indent=2).encode("utf8"))
