# encoding: utf-8
from APNSWrapper import *
import os
import re
import binascii
from  datetime  import  *  

import thread
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from friend.models import *
from forum.models import ThreadImage 
from forum.models import Thread
from forum.models import Like, Favor
from forum.models import Board 
from forum.models import UserInfo 
from forum.models import Reply 
from forum.models import UserThreadCount
from qa.models import *
from shop.models import Shop, Order, OrderItem, ItemComment
from shop.models import Item 
from shop.models import Promotion 
from shop.models import ShopCategory
from forum.models import AtMessage
import json
import httplib
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import logging
import time

format = '%(name)s %(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='/root/test/tea/home.log',level=logging.DEBUG,format=format)
logging.debug('begins:')

notification_queue = []

def get_grade(point):
    s = u"新手上路(" + str(point) + ")"
    if point > 500:
        s = u"正式茶友(" + str(point) + ")"
    if point > 1500:
        s = u"中级茶友(" + str(point) + ")"
    if point > 3000:
        s = u"高级茶友(" + str(point) + ")"
    return s


def notify_thread():
    logging.debug("notify_thread started")
    global notification_queue
    while True:
        time.sleep(2)
        logging.debug("inside while loop")
        queue2 = []
        # lock required
        try:
            for username in notification_queue:
                queue2.append(username)
        except:
            logging.debug("except")
        logging.debug("inside while loop1")
        notification_queue = []
        # unlock
        try:
            logging.debug(queue2)
            for x in queue2:
                try:
                    logging.debug("notify")
                    logging.debug(x["username"])
                    user = User.objects.get(username=x["username"])
                    logging.debug("notify 2")
                    deviceid = user.userinfo.deviceid
                    wrapper = APNSNotificationWrapper('/root/test/tea/cert.pem',
                                                      sandbox=False)
                    logging.debug("notify 3")
                    logging.debug("2")
                    if deviceid == "":
                        continue
                    logging.debug("3")
                    deviceToken = binascii.unhexlify(deviceid)
                    # create message
                    message = APNSNotification()
                    message.token(deviceToken)
                    message.alert(x["text"].encode('utf-8'))
                    logging.debug(x["text"])
                    messages = AtMessage.objects.filter(user=user,
                                                        read_status='unread',
                                                       )

                    message.badge(messages.count())
                    logging.debug("badge " + str(messages.count()))
                    message.sound()
                    # add message to tuple and send it to APNS server
                    wrapper.append(message)
                    wrapper.notify()
                except:
                    logging.debug("user except when notification")
                    continue
        except:
            logging.debug("except in for")
        logging.debug("inside while loop3")

    logging.debug("leave the thread")
    return

def notify_all_users(text):
    users = User.objects.all()
    for user in users:
        notify_one_user(user.username, text)
    return

logging.debug("start_new_thread")
thread.start_new_thread(notify_thread, ())

def user_point(username, point):
    user = User.objects.get(username=username)

    user.userinfo.point = user.userinfo.point + point
    user.userinfo.save()

    return

def notify_one_user(username, text):
    global notification_queue
    print "begin notify_one_user"
    notification_queue.append({"username":username, "text":text})
    return

def add_one_message(username, type, text, from_id):
    logging.debug("add_one_message " + username);
    user = User.objects.get(username=username)
    messages = AtMessage.objects.filter(user=user,
                                        type=type,
                                        from_id=from_id,
                                        read_status='unread',
                                       )
    notify_one_user(username, text)
    if len(messages) > 0:
        return

    message = AtMessage(
        user=user,
        type=type,
        text=text,
        from_id=from_id,
    )
    message.save()
    return

def article_html(request,id, template="article.html"):
    article = Document.objects.get(id=int(id))

    ctx = {"ret":"ok",
           "id":article.id,
           "title":article.name,
           "content":article.text,
           "create_time":str(article.create_time),
          }

    return render_to_response(template,
                              context_instance=RequestContext(request,
                                                              ctx))


def item_html(request,id, template="item.html"):
    item = Item.objects.get(id=int(id))

    ctx = {"ret":"ok",
           "id":item.id,
           "title":item.title,
           "content":item.content,
           "create_time":str(item.create_time),
          }

    return render_to_response(template,
                              context_instance=RequestContext(request,
                                                              ctx))


def shop_html(request,id, template="shop.html"):
    shop = Shop.objects.get(id=int(id))

    ctx = {"ret":"ok",
           "id":shop.id,
           "title":shop.title,
           "desc":shop.shop_desc,
           "username":shop.owner.username,
           "create_time":str(shop.create_time),
          }

    return render_to_response(template,
                              context_instance=RequestContext(request,
                                                              ctx))


def question_html(request,id, template="question.html"):
    question = Question.objects.get(id=int(id))
    comments = Answer.objects.filter(question=question).order_by('-id')
    cc = []
    for comment in comments:
        c = {"username":comment.user.username,
             "id":comment.id,
             "content":comment.content,
             "create_time":str(comment.create_time),
            }
        cc.append(c)

    ctx = {"ret":"ok",
           "id":question.id,
           "title":question.title,
           "content":question.content,
           "images":question.images_1,
           "username":question.user.username,
           "create_time":str(question.create_time),
           "comments":cc,
          }

    return render_to_response(template,
                              context_instance=RequestContext(request,
                                                              ctx))

def thread_html(request,id, template="thread.html"):
    thread = Thread.objects.get(id=int(id))
    comments = Reply.objects.filter(thread=thread).order_by('id')
    cc = []
    for comment in comments:
        iii = comment.images_1.split(',')
        images = []
        for ii in iii:
            images.append(ii)
        c = {"username":comment.user.username,
            "nickname":comment.user.userinfo.nickname,
             "id":comment.id,
             "images":images,
             "thumb":comment.user.userinfo.thumb,
             "content":comment.content,
             "create_time":str(comment.create_time),
            }
        cc.append(c)

    iii = thread.images_1.split(',')
    images = []
    for ii in iii:
        if ii != '':
            images.append(ii)

    ctx = {"ret":"ok",
            "nickname":thread.user.userinfo.nickname,
            "grade":get_grade(thread.user.userinfo.point),
           "thumb":thread.user.userinfo.thumb,
           "id":thread.id,
           "title":thread.title,
           "content":thread.content,
           "images":images,
           "username":thread.user.username,
           "create_time":str(thread.create_time),
           "comments":cc,
          }

    return render_to_response(template,
                              context_instance=RequestContext(request,
                                                              ctx))
def update_userinfo(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    desc = request.GET.get('desc')
    nickname = request.GET.get('nickname')
    thumb = request.GET.get('thumb', '')
    password = request.GET.get('password')

    try:
        uis = UserInfo.objects.get(nickname=nickname)
    except:
        uis = None
    if uis != None and uis.user.username != username:
        logging.debug("nickname dup")
        ret = "failed"
        str1 = json.dumps({"ret":ret, "reason":u"昵称已经被人使用"})
        return HttpResponse(str1)
    user = User.objects.get(username=username)
    try:
        userinfo = UserInfo.objects.get(user=user) 
    except:
        pass

    userinfo.user_desc = desc
    userinfo.thumb = thumb
    userinfo.nickname = nickname

    userinfo.save()

    ret = "ok"
    str1 = json.dumps({"ret":ret})
    return HttpResponse(str1)

def get_userinfo(request):
    username = request.GET.get('username')

    user = User.objects.get(username=username)
    try:
        userinfo = UserInfo.objects.get(user=user) 
    except:
        userinfo = UserInfo(user=user,
                            point=0
                           )

    ret = {"ret":"ok",
           "nickname":userinfo.nickname,
           "thumb":userinfo.thumb,
           "desc":userinfo.user_desc,
           "point":userinfo.point,
           "grade":get_grade(userinfo.point),
          }

    str1 = json.dumps(ret)
    return HttpResponse(str1)

def login_user(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    deviceid = request.GET.get('deviceid')

    logging.debug("device id " + deviceid)
    user = authenticate(username=username, password=password)
    aaa = 'ok'

    if user ==  None:
        aaa = 'failed'
    else:
        if len(deviceid) > 10:
            user.userinfo.deviceid = deviceid
        user.userinfo.save()

    ret = {"ret":aaa}

    str1 = json.dumps(ret)
    return HttpResponse(str1)

def reg_user(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    aaa = 'ok'
    try:
        user = User.objects.create_user(username, username + '@hhhh.com', password)
        userinfo = UserInfo(user=user,
                            nickname=username,
                            point=0)
        userinfo.save()
    except Exception, e:
	logging.debug(e)
        aaa = 'failed'

    ret = {"ret":aaa}

    str1 = json.dumps(ret)
    return HttpResponse(str1)

def get_shop(request):
    id = request.GET.get('shop')
    shop = Item.objects.get(id=int(id))
    a = {"title":shop.title,
         "price":shop.price,
         "id":shop.id,
         "content":shop.content,
         "sold":shop.sold,
        }

    str1 = json.dumps(a)
    return HttpResponse(str1)

def get_all_item_comments(request):
    page = request.GET.get("page", 1)
    comments = ItemComment.objects.all().order_by('-id')

    paginator = Paginator(comments, 10)
    cc = []
    try:
        for comment in paginator.page(page).object_list:
            c = {
                "id":comment.id,
                "username":comment.owner.username,
                "thumb":comment.owner.userinfo.thumb,
                "nickname":comment.owner.userinfo.nickname,
                "item_title":comment.item.title,
                "title":comment.title,
                "content":comment.content,
                "images":comment.images,
                "create_time":str(comment.create_time),
                "ziwei":comment.ziwei,
                "xiangqi":comment.xiangqi,
                "naipao":comment.naipao,
                "yexing":comment.yexing,
            }
            cc.append(c)
    except:
        print "page no for all comments"

    str1 = json.dumps(cc)
    return HttpResponse(str1)

def get_item_comments(request):
    id = request.GET.get('item')
    item = Item.objects.get(id=int(id))
    comments = ItemComment.objects.filter(item=item).order_by('-id')

    cc = []
    for comment in comments:
        user = comment
        c = {
            "id":comment.id,
            "username":comment.owner.username,
            "thumb":comment.owner.userinfo.thumb,
            "nickname":comment.owner.userinfo.nickname,
            "item_title":comment.item.title,
            "title":comment.title,
            "content":comment.content,
            "images":comment.images,
            "create_time":str(comment.create_time),
            "ziwei":comment.ziwei,
            "xiangqi":comment.xiangqi,
            "naipao":comment.naipao,
            "yexing":comment.yexing,
        }
        cc.append(c)

    str1 = json.dumps(cc)
    return HttpResponse(str1)


def get_item(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    id = request.GET.get('item')
    item = Item.objects.get(id=int(id))
    favor = False
    try:
        ll = Favor.objects.get(user=user, type="item",
                               from_id=item.id)
        if ll != None:
            favor = True
        else:
            favor = False
    except:
        pass
    like = False
    try:
        ll = Like.objects.get(user=user, type="item",
                              from_id=item.id)
        if ll != None:
            like = True
        else:
            like = False
    except:
        pass
    like_count = 0
    try:
        ll = Like.objects.filter(type="item",
                                 from_id=item.id)
        if ll != None:
            like_count = ll.count()
    except:
        pass
    favor_count = 0
    try:
        ll = Favor.objects.filter(type="item",
                                  from_id=item.id)
        if ll != None:
            favor_count = ll.count()
    except:
        pass


    a = {"title":item.title,
         "like":like,
         "favor":favor,
         "like_count":like_count,
         "favor_count":favor_count,
         "price":item.price,
         "id":item.id,
         "images":item.images,
         "content":item.content,
         "sold":item.sold,
        }

    str1 = json.dumps(a)
    return HttpResponse(str1)

def get_thread(request):
    thread_id = request.GET.get('thread')
    username = request.GET.get('username')
    thread = Thread.objects.get(id=int(thread_id))
    comments = Reply.objects.filter(thread=thread).order_by('id')
    try:
        user = User.objects.get(username=username)
    except:
        pass

    cc = []
    for comment in comments:
        c = {"username":comment.user.username,
             "nickname":comment.user.userinfo.nickname,
             "grade":get_grade(comment.user.userinfo.point),
             "thumb":comment.user.userinfo.thumb,
             "id":comment.id,
             "images":comment.images_1,
             "content":comment.content,
             "create_time":str(comment.create_time),
            }
        cc.append(c)

    favor = False
    try:
        ll = Favor.objects.get(user=user, type="thread",
                               from_id=int(thread_id))
        if ll != None:
            favor = True
        else:
            favor = False
    except:
        pass

    like = False
    try:
        ll = Like.objects.get(user=user, type="thread",
                              from_id=int(thread_id))
        if ll != None:
            like = True
        else:
            like = False
    except:
        pass

    like_count = 0
    try:
        ll = Like.objects.filter(type="thread",
                              from_id=int(thread_id))
        if ll != None:
            like_count = ll.count()
    except:
        pass

    favor_count = 0
    try:
        ll = Favor.objects.filter(type="thread",
                              from_id=int(thread_id))
        if ll != None:
            favor_count = ll.count()
    except:
        pass


    ret = {"ret":"ok",
           "like":like,
           "favor":favor,
           "like_count":like_count,
           "favor_count":favor_count,
           "id":thread.id,
           "images":thread.images_1,
           "title":thread.title,
           "content":thread.content,
           "images":thread.images_1,
           "username":thread.user.username,
           "nickname":thread.user.userinfo.nickname,
           "grade":get_grade(thread.user.userinfo.point),
           "thumb":thread.user.userinfo.thumb,
           "create_time":str(thread.create_time),
           "comments":cc,
          }

    try:
        user = User.objects.get(username=username)
        messages = AtMessage.objects.filter(user=user,
                                            type='forum',
                                            from_id=thread_id,
                                            read_status='unread',
                                           )
        logging.debug('type = forum, from_id = ' + str(thread_id) + 
                      ' uername = ' + username)
        for m in messages:
            m.read_status = 'read'
            m.save()
    except:
        logging.debug("get_thread didnt' find the message")

    str1 = json.dumps(ret)
    return HttpResponse(str1)

def get_question(request):
    id = request.GET.get('question')
    record = Question.objects.get(id=int(id))
    answers = []
    aaa = Answer.objects.filter(question=record).order_by('-id')
    for a in aaa:
        answer = {
            "content":a.content,
            "images":a.images_1,
            "username":a.user.username,
            "nickname":a.user.userinfo.nickname,
            "thumb":a.user.userinfo.thumb,
            "create_time":str(a.create_time),
            "accepted":a.accepted,
            "id":a.id,
        }
        answers.append(answer)

    question = {
        "title":record.title,
        "content":record.content,
        "images":record.images_1,
        "ended":record.ended,
        "username":record.user.username,
        "nickname":record.user.userinfo.nickname,
        "thumb":record.user.userinfo.thumb,
        "create_time":str(record.create_time),
        "id":record.id,
        "answers":answers,
    }

    str1 = json.dumps(question)
    return HttpResponse(str1)

def get_questions(request):
    page = request.GET.get("page", 1)
    page = int(page)
    if "category" in request.GET:
        id = request.GET.get("category")
        id = int(id)
        category = Category.objects.get(id=id)
        records = Question.objects.filter(category=category).order_by('-id')
    else:
        records = Question.objects.all().order_by('-id')

    paginator = Paginator(records, 10)
    questions = []
    try:
        for record in paginator.page(page).object_list:
            answers = []
            aaa = Answer.objects.filter(question=record).order_by('-id')
            for a in aaa:
                answer = {
                    "content":a.content,
                    "username":a.user.username,
                    "nickname":a.user.userinfo.nickname,
                    "thumb":a.user.userinfo.thumb,
                    "create_time":str(a.create_time),
                    "accepted":a.accepted,
                    "id":a.id,
                }
                answers.append(answer)
            ar = {
                "title":record.title,
                "cat":record.category.name,
                "content":record.content,
                "username":record.user.username,
                "nickname":record.user.userinfo.nickname,
                "thumb":record.user.userinfo.thumb,
                "create_time":str(record.create_time),
                "ended":record.ended,
                "id":record.id,
                "answers":answers,
            }
            questions.append(ar)
    except:
        print "page no"

    str1 = json.dumps(questions)
    return HttpResponse(str1)

def get_all_items(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    type = request.GET.get('type', 'normal')

    items = []
    aa = []
    if type == "normal":
        shops = Shop.objects.filter(active=True)
        for shop in shops:
            records = ShopCategory.objects.filter(shop=shop).order_by('-index3')
            for record in records:
                ii = Item.objects.filter(category=record).order_by('-id')
                for i in ii:
                    items.append(i)
    elif type == "favor":
        his_username = request.GET.get('his_username')
        try:
            his_user = User.objects.get(username=his_username)
        except:
            his_user = None

        rrr = Favor.objects.filter(user=his_user, type='item')
        for rr in rrr:
            try:
                ii = Item.objects.get(id=rr.from_id)
                items.append(ii)
            except:
                pass
        logging.debug("len = " + str(len(items)))

    for item in items:
        favor = False
        try:
            ll = Favor.objects.get(user=user, type="item",
                                   from_id=item.id)
            if ll != None:
                favor = True
            else:
                favor = False
        except:
            pass
        like = False
        try:
            ll = Like.objects.get(user=user, type="item",
                                  from_id=item.id)
            if ll != None:
                like = True
            else:
                like = False
        except:
            pass
        like_count = 0
        try:
            ll = Like.objects.filter(type="item",
                                     from_id=item.id)
            if ll != None:
                like_count = ll.count()
        except:
            pass
        favor_count = 0
        try:
            ll = Favor.objects.filter(type="item",
                                      from_id=item.id)
            if ll != None:
                favor_count = ll.count()
        except:
            pass

        a = {"title":item.title,
             "like":like,
             "favor":favor,
             "like_count":like_count,
             "favor_count":favor_count,
             "price":item.price,
             "id":item.id,
             "images":item.images,
             "content":item.content,
             "sold":item.sold,
            }
        aa.append(a)
    str1 = json.dumps(aa)
    return HttpResponse(str1)

def get_shop_cats(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    shop_id = request.GET.get("shop")
    shop = Shop.objects.get(id=int(shop_id))
    records = ShopCategory.objects.filter(shop=shop).order_by('-index3')
    cats = []
    for record in records:
        items = Item.objects.filter(category=record)
        aa = []
        for item in items:
            favor = False
            try:
                ll = Favor.objects.get(user=user, type="item",
                                       from_id=item.id)
                if ll != None:
                    favor = True
                else:
                    favor = False
            except:
                pass
            like = False
            try:
                ll = Like.objects.get(user=user, type="item",
                                      from_id=item.id)
                if ll != None:
                    like = True
                else:
                    like = False
            except:
                pass
            like_count = 0
            try:
                ll = Like.objects.filter(type="item",
                                         from_id=item.id)
                if ll != None:
                    like_count = ll.count()
            except:
                pass
            favor_count = 0
            try:
                ll = Favor.objects.filter(type="item",
                                          from_id=item.id)
                if ll != None:
                    favor_count = ll.count()
            except:
                pass

            a = {"title":item.title,
                 "like":like,
                 "favor":favor,
                 "like_count":like_count,
                 "favor_count":favor_count,
                 "price":item.price,
                 "id":item.id,
                 "images":item.images,
                 "sold":item.sold,
                 "content":item.content,
                }
            aa.append(a)
        ar = {
            "name":record.name,
            "index":record.index3,
            "id":record.id,
            "items":aa,
        }
        cats.append(ar)

    str1 = json.dumps(cats)
    return HttpResponse(str1)

def get_qa_cats(request):
    records = QACategory.objects.all()
    boards = []
    for record in records:
        ar = {
            "name":record.name,
            "id":record.id,
        }
        boards.append(ar)

    str1 = json.dumps(boards)
    return HttpResponse(str1)

def get_promotions(request):
    records = Promotion.objects.all()
    promotions = []
    for record in records:
        ar = {
            "image_name":record.image_name,
            "shop":record.shop.id,
            "item":record.item.id,
        }
        promotions.append(ar)

    str1 = json.dumps(promotions)
    return HttpResponse(str1)

def get_shops(request):
    type = request.GET.get('type', 'normal')
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    if type == "normal":
        records = Shop.objects.filter(active=True)
    elif type == "favor":
        his_username = request.GET.get('his_username')
        try:
            his_user = User.objects.get(username=his_username)
        except:
            his_user = None
        rrr = Favor.objects.filter(user=his_user)
        records = []
        for rr in rrr:
            try:
                record = Shop.objects.get(id=rr.from_id)
                if record.active == True:
                    records.append(record)
            except:
                pass

    shops = []
    for record in records:
        favor = False
        try:
            ll = Favor.objects.get(user=user, type="shop",
                                   from_id=record.id)
            if ll != None:
                favor = True
            else:
                favor = False
        except:
            pass
        like = False
        try:
            ll = Like.objects.get(user=user, type="shop",
                                  from_id=record.id)
            if ll != None:
                like = True
            else:
                like = False
        except:
            pass
        like_count = 0
        try:
            ll = Like.objects.filter(type="shop",
                                     from_id=record.id)
            if ll != None:
                like_count = ll.count()
        except:
            pass
        favor_count = 0
        try:
            ll = Favor.objects.filter(type="shop",
                                      from_id=record.id)
            if ll != None:
                favor_count = ll.count()
        except:
            pass

        ar = {
            "like":like,
            "like_count":like_count,
            "favor_count":favor_count,
            "favor":favor,
            "title":record.title,
            "desc":record.shop_desc,
            "id":record.id,
        }
        shops.append(ar)

    str1 = json.dumps(shops)
    return HttpResponse(str1)

def get_boards(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    records = Board.objects.filter(active=True).order_by('index3')
    boards = []
    for record in records:
        nr_thread = Thread.objects.filter(board=record).count()
        if user != None:
            try:
                readcount = UserThreadCount.objects.get(board=record, user=user)
                if nr_thread > readcount.readed_count:
                    nr_unread = nr_thread - readcount.readed_count
                else:
                    nr_unread = 0
            except:
                nr_unread = nr_thread
        else:
            nr_unread = nr_thread
        ar = {
            "name":record.name,
            "desc":record.board_desc,
            "nr_thread":nr_thread,
	        "nr_unread_thread":nr_unread,
            "id":record.id,
        }
        boards.append(ar)

    str1 = json.dumps(boards)
    return HttpResponse(str1)

def post_item_comment(request):
    item_id = request.GET.get('item')
    title = request.GET.get('title')
    content = request.GET.get('content')
    images = request.GET.get('images')
    xiangqi = request.GET.get('xiangqi')
    ziwei = request.GET.get('ziwei')
    naipao = request.GET.get('naipao')
    yexing = request.GET.get('yexing')

    username = request.GET.get('username')
    password = request.GET.get('password')
 
    user = User.objects.get(username=username)
    item = Item.objects.get(id=int(item_id))
    comment = ItemComment(
                owner=user,
                item=item,
                title=title,
                images=images,
                content=content,
                xiangqi=int(xiangqi),
                ziwei=int(ziwei),
                naipao=int(naipao),
                yexing=int(yexing),
                )
    comment.save()
    ret = {"ret":"ok"}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def like(request):
    cmd = request.GET.get('cmd')
    id = request.GET.get('id')
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    password = request.GET.get('password')
    type = request.GET.get('type')

    if cmd == "like" or cmd == "unlike":
        repo = Like
    else:
        repo = Favor
 
    if cmd == "like" or cmd == "favor":
        try:
            one = repo.objects.get(user=user,from_id=int(id),type=type)
        except:
            one = None
        if one != None:
            ret = {"ret":"already have"}
            str1 = json.dumps(ret)
            return HttpResponse(str1)
        like = repo(
            user=user,
            from_id=id,
            type=type,
        )
        like.save()
        ret = {"ret":"ok"}
        str1 = json.dumps(ret)
        return HttpResponse(str1)

    if cmd == "unlike" or cmd == "unfavor":
        try:
            one = repo.objects.get(user=user,from_id=int(id),type=type)
            one.delete()
        except:
            pass
        ret = {"ret":"ok"}
        str1 = json.dumps(ret)
        return HttpResponse(str1)

def post_answer(request):
    question_id = request.GET.get('question')
    content = request.GET.get('content')
    username = request.GET.get('username')
    password = request.GET.get('password')
    images = request.GET.get('images')
 
    user = User.objects.get(username=username)
    question = Question.objects.get(id=int(question_id))
    answer = Answer(
                user=user,
                question=question,
                images_1=images,
                content=content,
                )
    answer.save()
    ret = {"ret":"ok"}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def post_reply(request):
    thread_id = request.GET.get('thread')
    content = request.GET.get('content')
    username = request.GET.get('username')
    images = request.GET.get('images', '')
    password = request.GET.get('password')

    atnicknames = re.findall(r'@(\S+)', content)
    atusers = []
    for atn in atnicknames:
        try:
            uin = UserInfo.objects.get(nickname=atn)
            atusers.append(uin.user)
        except:
            uin = None

    user_point(username, 1)
    user = User.objects.get(username=username)
    thread = Thread.objects.get(id=int(thread_id))
    reply = Reply(
                user=user,
                thread=thread,
                content=content,
                images_1=images,
                )
    reply.save()
    thread.last_reply = reply.create_time
    thread.save()
    #notify the attendees
    already_users = [] 
    if username != thread.user.username:
        add_one_message(thread.user.username, 'forum',
                        u'[社区]您的主题有一个新的回复',
                        int(thread_id),
                       )
    user_point(thread.user.username, 1)
    already_users.append(thread.user.username)
    replys = Reply.objects.filter(thread=thread)
    for atu in atusers:
        if atu.username != username:
            if atu.username in already_users:
                continue
            already_users.append(atu.username)
            add_one_message(atu.username, 'forum',
                            u'[社区]您参与的主题有一个新的回复',
                            int(thread_id),
                           )
 
    ret = {"ret":"ok"}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def accept_answer(request):
    question_id = request.GET.get('question')
    answer_id = request.GET.get('answer')

    question = Question.objects.get(id=int(question_id))
    answer = Answer.objects.get(id=int(answer_id))

    username = request.GET.get('username')
    password = request.GET.get('password')

    user = User.objects.get(username=username)


    question.ended = True
    answer.accepted = True

    question.save()
    answer.save()
    ret = {"ret":"ok"}
    str1 = json.dumps(ret)

    return HttpResponse(str1)

def post_question(request):
    category_id = request.GET.get('category')
    title = request.GET.get('title')
    content = request.GET.get('content')
    images = request.GET.get('images', '')
    username = request.GET.get('username')
    password = request.GET.get('password')

    user = User.objects.get(username=username)

    category = QACategory.objects.get(id=int(category_id))
    question = Question(
                    user=user,
                    category=category,
                    title=title,
                    content=content,
                    images_1=images,
                   )

    question.save()
    ret = {"ret":"ok", "id":question.id}
    str1 = json.dumps(ret)

    return HttpResponse(str1)

def post_thread(request):
    board_id = request.GET.get('board')
    title = request.GET.get('title', '#')
    content = request.GET.get('content')
    images = request.GET.get('images', '')
    username = request.GET.get('username')
    password = request.GET.get('password')

    user = User.objects.get(username=username)

    board = Board.objects.get(id=int(board_id))
    thread = Thread(
                    user=user,
                    board=board,
                    title=title,
                    content=content,
                    images_1=images,
                    last_reply=datetime.now(),
                   )

    thread.save()

    atnicknames = re.findall(r'@(\S+)', content)
    atusers = []
    for atn in atnicknames:
        try:
            uin = UserInfo.objects.get(nickname=atn)
            atusers.append(uin.user)
        except:
            uin = None

    already_users = [] 
    for atu in atusers:
        if atu.username in already_users:
            continue
        already_users.append(atu.username)
        add_one_message(atu.username, 'forum',
                        u'[社区]' + content,
                        int(thread.id),
                       )
 
    #notify_all_users(u'社区有一条新贴子啦！')

    user_point(username, 5)
    ret = {"ret":"ok"}
    str1 = json.dumps(ret)

    return HttpResponse(str1)

def get_user_threads(request):
    page = request.GET.get("page", 1)
    page = int(page)
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    records = Thread.objects.filter(user=user).order_by('-id')

    paginator = Paginator(records, 10)
    threads = []

    try:
        for record in paginator.page(page).object_list:
            try:
                comments = Reply.objects.filter(thread=record).order_by('id')
                cc = []
                for comment in comments:
                    c = {
                        "username":comment.user.username,
                        "nickname":comment.user.userinfo.nickname,
                        "thumb":comment.user.userinfo.thumb,
                        "id":comment.id,
                        "images":comment.images_1,
                        "content":comment.content,
                        "create_time":str(comment.create_time),
                    }
                    cc.append(c)
                if record.user.userinfo.thumb == "(null)":
                    thumb = ""
                else:
                    thumb = record.user.userinfo.thumb
                ar = {
                    "username":record.user.username,
                    "nickname":record.user.userinfo.nickname,
                    "grade":get_grade(record.user.userinfo.point),
                    "thumb":thumb,
                    "id":record.id,
                    "title":record.title,
                    "content":record.content,
                    "last_reply":str(record.last_reply),
                    "images":record.images_1,
                    "create_time":str(record.create_time),
                    "comments":cc,
                }
                threads.append(ar)
            except:
                logging.debug("get_user_threads exception")
    except:
        logging.debug("page no")

    str1 = json.dumps(threads)
    return HttpResponse(str1)

def get_threads(request):
    type = request.GET.get("type", "board")
    page = request.GET.get("page", 1)
    page = int(page)

    try:
        username = request.GET.get('username')
        user = User.objects.get(username=username)
    except:
        logging.debug("get_threads user except")
        user = None

    if type == "board":
        board_id = request.GET.get('board')
        board = Board.objects.get(id=int(board_id))
        records = Thread.objects.filter(board=board).order_by('-last_reply')
        if user != None:
            try:
                readcount = UserThreadCount.objects.get(user=user,board=board)
                readcount.readed_count = records.count()
            except:
                logging.debug("get_threads readcount except")
                readcount = UserThreadCount(user=user,board=board,readed_count=records.count())
            readcount.save()
    elif type == "favor":
        records = []
        rrr = Favor.objects.filter(user=user, type="thread").order_by('-id')
        for rr in rrr:
            thread = Thread.objects.get(id=rr.from_id)
            records.append(thread)
    elif type == "user_thread":
        try:
            his_username = request.GET.get('his_username')
            his_user = User.objects.get(username=his_username)
        except:
            his_user = None
        records = Thread.objects.filter(user=his_user).order_by('-last_reply')

    paginator = Paginator(records, 10)
    threads = []

    try:
        for record in paginator.page(page).object_list:
            try:
                logging.debug("0")
                comments = Reply.objects.filter(thread=record).order_by('id')
                cc = []
                for comment in comments:
                    c = {
                        "username":comment.user.username,
                        "nickname":comment.user.userinfo.nickname,
                        "thumb":comment.user.userinfo.thumb,
                        "id":comment.id,
                        "images":comment.images_1,
                        "content":comment.content,
                        "create_time":str(comment.create_time),
                    }
                    cc.append(c)
                if record.user.userinfo.thumb == "(null)":
                    thumb = ""
                else:
                    thumb = record.user.userinfo.thumb
                logging.debug("1")

                favor = False
                try:
                    ll = Favor.objects.get(user=user, type="thread",
                                      from_id=record.id)
                    if ll != None:
                        favor = True
                    else:
                        favor = False
                except:
                    pass

                like = False
                try:
                    ll = Like.objects.get(user=user, type="thread",
                                      from_id=record.id)
                    if ll != None:
                        like = True
                    else:
                        like = False
                except:
                    pass

                like_count = 0
                try:
                    ll = Like.objects.filter(type="thread",
                                      from_id=record.id)
                    if ll != None:
                        like_count = ll.count()
                except:
                    pass
                favor_count = 0
                try:
                    ll = Favor.objects.filter(type="thread",
                                      from_id=record.id)
                    if ll != None:
                        favor_count = ll.count()
                except:
                    pass

                logging.debug("2")

                ar = {
                    "username":record.user.username,
                    "nickname":record.user.userinfo.nickname,
                    "grade":get_grade(record.user.userinfo.point),
                    "thumb":thumb,
                    "id":record.id,
                    "title":record.title,
                    "content":record.content,
                    "last_reply":str(record.last_reply),
                    "images":record.images_1,
                    "create_time":str(record.create_time),
                    "like":like,
                    "like_count":like_count,
                    "favor_count":favor_count,
                    "favor":favor,
                    "comments":cc,
                }
                threads.append(ar)
                logging.debug("3")
            except Exception,e:
                logging.debug("get_threads exception")
                logging.debug(e)
                continue
    except:
        logging.debug("page no")

    str1 = json.dumps(threads)
    return HttpResponse(str1)


def get_bigpictures(request):
    page = request.GET.get("page", 1)
    page = int(page)
    print page
    records = Bigpicture.objects.all().order_by('-id')
    paginator = Paginator(records, 10)
    articles = []
    try:
        for record in paginator.page(page).object_list:
            ar = {
                "id":record.id,
                "pic_url":record.pic_url,
                "link":record.link.replace(' ', ''),
            }
            articles.append(ar)
    except:
        print "page no"

    str1 = json.dumps(articles)
    return HttpResponse(str1)

def get_articles(request):
    page = request.GET.get("page", 1)
    page = int(page)
    print page
    records = Document.objects.all().order_by('-id')
    paginator = Paginator(records, 10)
    articles = []
    try:
        for record in paginator.page(page).object_list:
            ar = {
                "id":record.id,
                "pic_url":record.pic_url,
                "name":record.name,
                "summary":record.summary,
                "text":record.text.replace(' ', ''),
            }
            articles.append(ar)
    except:
        print "no result"

    str1 = json.dumps(articles)
    return HttpResponse(str1)

@csrf_exempt
def save_file(request): 
    logging.debug("save_file")
    id = "49"
    thread = Thread.objects.get(id=int(id))
    threadimage = ThreadImage(thread=thread)
    file_content = ContentFile(request.FILES['image'].read()) 
    logging.debug(request.FILES['image'].name)
    threadimage.image.save(request.FILES['image'].name, file_content)
    
    logging.debug(request.FILES['image'].name)
    filename = threadimage.image.name.replace('threadimages/', '')
    orig_filename = '/root/bak/satchmo/mystore/store/static/tea/threadimages/' + filename
    after_filename = orig_filename + '.thumb.jpg'
    os.system("convert -resize 100x " + orig_filename + " " + after_filename)
    ret = {"ret":"ok", "name":filename}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def new_order(request): 
    username = request.GET.get('username')

    addr = request.GET.get('addr')
    phone = request.GET.get('phone')
    contact = request.GET.get('contact')
    pay = request.GET.get('pay')

    password = request.GET.get('password')
    items_string = request.GET.get('items')
    user = User.objects.get(username=username)
    order = Order(owner=user,
                  addr=addr,
                  phone=phone,
                  contact=contact,
                  total=0)
    order.save()
    total = 0

    for ii in items_string.split(',,'):
        dd = ii.split(',')
        item_id = int(dd[0])
        count = int(dd[1])
        item = Item.objects.get(id=item_id)
        order_item = OrderItem(item=item,
                               count=count,
                               order=order,
                              )
        order_item.save()
        subtotal = item.price * count
        total = total + subtotal

    order.total = total
    order.save()
    ret = {"ret":"ok", "id":order.id}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def mark_read_atmessage(request): 
    username = request.GET.get('username')
    atmessage = request.GET.get('atmessage')
    user = User.objects.get(username=username)

    atmessage = AtMessage.objects.get(id=int(atmessage))
    atmessage.read_status = 'read'
    atmessage.save()

    ret = {"ret":"ok"}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def get_user_atmessages(request): 
    username = request.GET.get('username')
    user = User.objects.get(username=username)

    atmessages = AtMessage.objects.filter(user=user).order_by('-id')[:30]
    oo = []
    for atmessage in atmessages:
        o = {"id":atmessage.id,
             "type":atmessage.type,
             "read_status":atmessage.read,
             "text":atmessage.text,
             "from_id":atmessage.from_id,
            }
        oo.append(o)
    ret = {"ret":"ok", "atmessages":oo}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def get_user_orders(request): 
    username = request.GET.get('username')
    user = User.objects.get(username=username)

    orders = Order.objects.filter(owner=user).order_by('-id')
    oo = []
    for order in orders:
        items = OrderItem.objects.filter(order=order) 
        ii = []
        for i in items:
            item = {"id":i.item.id,
                    "title":i.item.title,
                    "price":i.item.price,
                    "count":i.count,
                   }
            ii.append(item)
        o = {"id":order.id, "items":ii,
             "username":order.owner.username,
             "total":order.total,
             "addr":order.addr,
             #"pay":order.pay,
             "pay":u'货到付款',
             "status":order.status,
             "create_time":str(order.create_time),
             "phone":order.phone,
             "contact":order.contact,
            }
        oo.append(o)
    ret = {"ret":"ok", "orders":oo}
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def get_order(request): 
    id = request.GET.get("order")
    order = Order.objects.get(id=int(id))
    items = OrderItem.objects.filter(order=order) 
    ii = []
    for i in items:
        item = {"id":i.item.id,
                "title":i.item.title,
                "price":i.item.price,
                "count":i.count,
               }
        ii.append(item)

    ret = {"ret":"ok", "id":order.id, "items":ii,
           "username":order.owner.username,
           "total":order.total,
           "addr":order.addr,
           #"pay":order.pay,
           "pay":u'货到付款',
           "status":order.status,
           "create_time":str(order.create_time),
           "phone":order.phone,
           "contact":order.contact,
          }
    str1 = json.dumps(ret)
    return HttpResponse(str1)

def set_discount(request):
    from shop.models import Item 
    items = Item.objects.all()
    for item in items:
        item.sold = 0
        item.save()

    ret = {"ret":"ok"}
    str1 = json.dumps(ret)
    return HttpResponse(str1)


cmd_dict = {
    "get_articles":get_articles,
    "get_bigpictures":get_bigpictures,
    "reg_user":reg_user,
    "login_user":login_user,
    "get_userinfo":get_userinfo,
    "update_userinfo":update_userinfo,
    "get_threads":get_threads,
    "post_thread":post_thread,
    "post_question":post_question,
    "accept_answer":accept_answer,
    "post_reply":post_reply,
    "post_answer":post_answer,
    "get_boards":get_boards,
    "get_shops":get_shops,
    "get_promotions":get_promotions,
    "get_questions":get_questions,
    "get_question":get_question,
    "get_item":get_item,
    "get_item_comments":get_item_comments,
    "post_item_comment":post_item_comment,
    "get_all_item_comments":get_all_item_comments,
    "get_thread":get_thread,
    "get_qa_cats":get_qa_cats,
    "get_shop_cats":get_shop_cats,
    "get_all_items":get_all_items,
    "new_order":new_order,
    "get_order":get_order,
    "set_discount":set_discount,
    "get_user_orders":get_user_orders,
    "get_user_threads":get_user_threads,
    "get_user_atmessages":get_user_atmessages,
    "mark_read_atmessage":mark_read_atmessage,
    "like":like,
    "unlike":like,
    "favor":like,
    "unfavor":like,
}

def process(request):
    logging.debug(request)
    cmd = request.GET.get('cmd', None)
    res = cmd_dict[cmd](request)
    return res

