# -*- coding: utf-8 -*-
import facebook
import re
import json


def CommentCrawler(graph, postid):
    total = 0
    commentlist = []
    args = {'fields': 'like_count, from, message, id, created_time, attachment', 'limit':50, 'after':''}

    COMMENTS = graph.get_object(postid + '/comments', **args)

    next_id = "nextPage"

    while next_id != "":
        total += len(COMMENTS['data'])
        for comment in COMMENTS['data']:
            commentlist.append({'id':comment['id'], 'like_count':comment['like_count'], 'Author':{'uid':comment['from']['id'], 'uname':comment['from']['name']}, 'time':comment['created_time'], 'msg':comment['message']})

        if 'paging' in COMMENTS and 'next' in COMMENTS['paging']:
            next_id = COMMENTS['paging']['cursors']['after'].encode('utf8')
        else:
            break

        args['after'] = next_id
        COMMENTS = graph.get_object(postid + '/comments', **args)

    print "Comments: " + str(total)
    return commentlist

def LikeCrawler(graph, postid):
    total = 0
    likelist = []
    args = {'limit':1000, 'after':'' }

    LIKES = graph.get_object(postid + '/likes', **args)

    next_id = "nextPage"

    while next_id != "":
        total += len(LIKES['data'])
        for person in LIKES['data']:
            likelist.append({ 'uid':person['id'], 'uname':person['name']})
        next_id = ""
        if 'paging' in LIKES and 'next' in LIKES['paging']:
            next_id = LIKES['paging']['cursors']['after'].encode('utf8')
        else:
            break

        args['after'] = next_id
        LIKES = graph.get_object(postid + '/likes', **args)

    print "Likes: " + str(total)

    return likelist, total


def crawing(graph, Fans_id, args):
    pattent = re.compile(u'[\U00010000-\U0010ffff]')
    next_id = ""
    messages = []
    posts = graph.get_object(Fans_id + '/posts', **args)

    next_id = "nextpage"

    while (next_id != ""):
        # iterate posts
        for post in posts['data']:
            post_id = post['id']
            # member of like
            likelist, likeCount = LikeCrawler(graph, post_id)
            commentlist = CommentCrawler(graph, post_id)
            messages.append({'id':post_id, 'like_count': likeCount, 'time':post['created_time'], 'likes':likelist, 'comments':commentlist})
        next_id = ''
        if ('paging' in posts):
            next_id = re.search('[0-9]+$', posts['paging']['next']).group(0)
        else:
            break

        print next_id
        args['until'] = next_id
        posts = graph.get_object(Fans_id + '/posts', **args)

    return messages

if __name__ == "__main__":
    out = open('Fans.txt', 'w')

    Token = 'CAACEdEose0cBANKH2QjO5gwXVYqikntPfPNH4F6iY7ZC8nLsIqsiPItZCytVWWclhOot6y3hXJIdLmOb2oVVawaPe3mZBRxo6kIBLDZCsBTkZBPo1mXzeevb0n4BrpNQdCCHqlG7VNWKF36HSTR8j2LPoCNp2ZCqbZBrSZAl0gBu51pGcjEcs1K3jIgwXNnW92rqRbMQW8RvXnU7a08JaIfJfW49qb49bkYZD'

    graph = facebook.GraphAPI(Token)

    #Fans_id = '544241848968882'
    Fans_id = '136845026417486'
    #Post_id = '544241848968882_810446749015056'

    args = {'fields' : 'id, message, likes, comments', 'limit' : 5, 'until' : ''}

    messages = crawing(graph, Fans_id, args)

    out.write(json.dumps(messages, ensure_ascii=False, indent=2).encode("utf8"))
