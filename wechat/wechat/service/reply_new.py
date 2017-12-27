# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: reply.py 
@time: 2017/12/1 14:37 
"""
from ..models import Reply,Resource,Resource_Cache,User
from django.db.models import Sum, Count,Avg
import logging
import datetime
import time
from ..crawler.mainprocess import keywordSearch
from ..comm_lib.crawlerTool import crawlerTool as ct
import re
from ..comm_lib.deal_exception import my_wrapfunc

logger = logging.getLogger('default')

@my_wrapfunc
def reply(MsgContent,userOpenId,mod=''):
    start = time.time()
    save_input(userOpenId,MsgContent,mod=mod)
    logger.debug('input:%s userId:%s mod:%s'%(MsgContent,str(userOpenId),mod))
    queryResult = search_resource(MsgContent,userOpenId,mod=mod)
    if queryResult:#这个逻辑后面得改，不兼容搜索，要么就是根据公众号类型不同返回
       return {'reply': queryResult, 'mode': 0}
    #reply = maRen()
    if mod == 'qgg':
        reply = crawler(MsgContent, userOpenId=userOpenId,sites=[30,31],mod=mod)
    elif mod == 'pan':
        reply = crawler(MsgContent, userOpenId=userOpenId,sites=[19],mod=mod)
    else:
        reply = crawler(MsgContent,userOpenId=userOpenId,sites=[19],mod=mod)
    if reply:
        return {'reply':reply,'mode':0}
    elif re.match('\s*\d+\s*',MsgContent):
        return {'reply': '没有搜到对应集数 请重新搜索作品名称（不要带集数）', 'mode': 1}
   # elif mod and mod != 'pan':
    #    return {'reply': '没有搜到结果,你可以在标题前加上 pan 搜索云盘内容，如"pan 权力的游戏" ', 'mode': 1}
    elif time.time() - start >5:#这个不太灵，因为搜索可能就会超过6秒
        return {'reply': '处理超时了，重试一次吧亲', 'mode': 1}
    else:
        return {'reply':'没有搜到结果','mode':1}

#处理输入图片的情况
@my_wrapfunc
def pic_reply(PicUrl):
 pass





#爬虫回复
@my_wrapfunc
def crawler(keyword,userOpenId='',sites=[19],mod=''):
    rsDict = keywordSearch(keyword,sites=sites)
    urlinfos = rsDict['urlinfos']
    rs = []
    for urlinfo in urlinfos:
        title = urlinfo.get('title','').replace("'",'"')
        url = urlinfo.get('url','')
        rs.append('''<a href='%s'>%s</a> '''%(url,title))
        if title and url:
            #save_resource_task.delay(title+'_'+mod,url,keyword,userOpenId=userOpenId)  #异步发现不靠谱
            save_resource(title + '_' + mod, url, keyword+ '_' + mod, userOpenId=userOpenId)
    return results_toString(rs,mod)

@my_wrapfunc
def results_toString(rs,mod=''):  #限制貌似是不能超过2048字节
    crawlerReply = ''
    strSum = 0
    if mod == 'qgg':
        rs.reverse()#倒序排列 这操作会改变原来的数组
        pass
    for resultStr in rs:
        if strSum > 1970:
            if mod == 'qgg':
                crawlerReply = crawlerReply + '有未显示集数，回复数字集数(如 1)从第n集开始显示'
            break
        for s in resultStr:
            if s.isdigit()|s.isalpha()|s.isspace():strSum+=1
            else:strSum+=4
            crawlerReply = crawlerReply + s
        crawlerReply = crawlerReply + '\n\n'
    return crawlerReply



@my_wrapfunc
def search_resource(queryString,userOpenId='',mod=''):
    #这里增加一个逻辑 如果用户输入数字，则先去数据库里搜索最近一分钟title包含 数字_的结果 按时间倒序排列
    now = datetime.datetime.now()

    if re.match('\s*\d+\s*',queryString):
        page = int(queryString)
        queryString = queryString.replace(' ','')
        start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        user = User.objects.filter(OpenID__iexact=userOpenId)
        if user: #利用user表保存keyword，防止异步 这里需要加个翻页的逻辑 后面用这种mod的模式不好
            user = user[0]
            keyword = user.keyword
            search_resource = Resource_Cache.objects.filter(create_time__gt=start).filter(keyword__iexact=keyword)
            logger.debug(keyword,search_resource)
            #.filter(title__endswith=' '+queryString + '_' + mod) 先拉出完整搜索结果存入数组
            rs_dict = {}
            resources=[]
            for r in search_resource:
                rs_page = ct.getRegex(" (\d+)_%s"%mod ,r.title)

                if rs_page:
                    rs_page=int(rs_page)
                    if rs_page >= page:
                        resources.append(r)
            resources.reverse()

        else:
            resources = Resource_Cache.objects.filter(create_time__gt=start).filter(OpenID__iexact=userOpenId).filter(title__endswith=' '+queryString + '_' + mod).order_by("-create_time")

    else:
        start = now-datetime.timedelta(hours=23, minutes=59, seconds=59)#缓存一天的数据 读取缓存需要修改用户id  缓存和上面的逻辑有冲突
        resources = Resource_Cache.objects.filter(create_time__gt=start).filter(keyword__iexact=queryString+'_'+mod) #应该显示不了30条吧

    result=[]

    for resource in resources:
        result.append('''<a href='%s'>%s</a> '''%(resource.url,resource.title.replace('_' + mod,'')))
        if resource.uploader != 'manual':#如果人工插入不更新
            resource.create_time = now
        resource.OpenID = userOpenId#这个是有问题的
        resource.save()


    output = results_toString(result,mod)
    return output



@my_wrapfunc
def save_resource(title,url,input,userOpenId='',uploader='system'):
    logger.debug('save a record %s %s %s %s'%(title,url,input,userOpenId))
    r = Resource_Cache.objects.get_or_create(keyword=input,url=url,OpenID=userOpenId)[0]#一个用户的同一搜索只能存一条
    r.title=title
    r.uploader = uploader
    r.create_time = datetime.datetime.now()
    r.save()


@my_wrapfunc
def save_input(userOpenId,input,mod=''):
    u=User.objects.get_or_create(OpenID=userOpenId)[0]

    u.last_input = input
    if not re.match('\s*\d+\s*',input):
        u.keyword = input+'_'+mod
    u.last_page = 1
    u.last_request_time = datetime.datetime.now()
    u.save()