# -*- coding: utf-8 -*-
from pymongo import MongoClient

import facebook
import json
import time
import sys
import re

def CommentCrawler(graph, postid):
    total = 0
    commentlist = []
    args = {'fields': 'like_count, from, message, id, created_time, attachment', 'limit':500, 'after':''}

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
        time.sleep(2.5)
        COMMENTS = graph.get_object(postid + '/comments', **args)

    print "Comments: " + str(total)
    return commentlist

def LikeCrawler(graph, postid):
    total = 0
    likelist = []
    args = {'limit':10000, 'after':'' }

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
        time.sleep(2.5)
        LIKES = graph.get_object(postid + '/likes', **args)

    print "Likes: " + str(total)

    return likelist, total


def crawing(graph, Fans_id, args, collections):
    next_id = ""
    counter = 0
    posts = graph.get_object(Fans_id + '/posts', **args)

    next_id = "nextpage"

    while (next_id != ""):
        # iterate posts
        for post in posts['data']:
            print counter
            counter +=1

            post_id = post['id']
            # Check the post if it exists
            if collections.find_one({'id':post_id}):
                continue

#            like_list, likeCount = LikeCrawler(graph, post_id)
#            comment_list = CommentCrawler(graph, post_id)

            if ('message' in post):
                msg = {'msg':post['message'], 'id':post_id, 'time':post['created_time']}
            else:
                msg = {'id':post_id, 'time':post['created_time']}


            collections.insert(msg)

        if ('paging' in posts):
            next_id = re.search('[0-9]+$', posts['paging']['next']).group(0)
        else:
            break

        print next_id
        args['until'] = next_id
        posts = graph.get_object(Fans_id + '/posts', **args)

    return counter

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "python Crawler.py <Token>"
    Token = sys.argv[1]
    graph = facebook.GraphAPI(Token)

    collection = MongoClient().facebook_fans_db.KP_Msg

    if collection:
        print 'Database Online'


    Fans_id = '136845026417486'

    args = {'fields' : 'id, message, likes, comments', 'limit' : 50, 'until' : ''}

    post_count = crawing(graph, Fans_id, args, collection)

    #out.write(json.dumps(messages, ensure_ascii=False, indent=2).encode("utf8"))
