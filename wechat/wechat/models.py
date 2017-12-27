# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


# Create your models here.


class Reply(models.Model):
    reply = models.CharField(max_length=100)
    weight = models.IntegerField()
    update_time = models.DateTimeField('events time',blank=True)
    create_time = models.DateTimeField(auto_now=True,blank=True)  # 创建时间(自动获取当前时间)

    def __unicode__(self): # 将对象以str的方式显示出来
            # 在Python3中使用 def __str__(self):
            return self.reply

#原意是用于固定回复，后逻辑改为通过缓存表uploader = manual实现 故该表目前没用到
class Resource(models.Model):
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    page = models.TextField(blank=True)
    post_date =  models.CharField(max_length=255,blank=True)
    request_count=  models.IntegerField(default=1)
    update_time = models.DateTimeField('events time',blank=True)
    create_time = models.DateTimeField(auto_now=True,blank=True,db_index = True)  # 创建时间(自动获取当前时间)
    verify_time = models.DateTimeField('verify time',blank=True)
    user = models.CharField(max_length=100,blank=True)#对应api的
    uploader = models.CharField(max_length=100,blank=True)#对应api的
    type = models.CharField(max_length=100, blank=True)#以,分割各种类型
    OpenID = models.CharField(max_length=100, blank=True)
    UnionID = models.CharField(max_length=100, blank=True)

    def __unicode__(self): # 将对象以str的方式显示出来
            # 在Python3中使用 def __str__(self):
            return self.url+self.title

#用户状态表
class User(models.Model):
    name = models.CharField(max_length=100, blank=True)
    OpenID = models.CharField(max_length=100, blank=True,unique= True)
    UnionID = models.CharField(max_length=100, blank=True)
    last_input = models.CharField(max_length=100, blank=True)#用户上次输入
    keyword = models.CharField(max_length=100, blank=True)#用户当前关键输入
    status = models.CharField(max_length=100, blank=True)  # 用户当前功能状态
    last_page = models.IntegerField(default=1, blank=True)
    last_request_time = models.DateTimeField(auto_now=True,blank=True)
    cache_page = models.TextField(blank=True)  #用于保存微信没有显示的内容


#用户日志表 用于支持更复杂的上下文功能
class User_Log(models.Model):
    OpenID = models.CharField(max_length=100, blank=True)
    last_input = models.CharField(max_length=100, blank=True)#用户上次输入
    keyword = models.CharField(max_length=100, blank=True)#用户当前关键输入
    request_time = models.DateTimeField(auto_now=True,blank=True)
    last_output = models.TextField(blank=True)  #用于保存微信没有显示的内容
    status = models.CharField(max_length=100, blank=True)  # 用户当前功能状态


#资源缓存表  一个keyword对应多条cache
class Resource_Cache(models.Model):
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    page = models.TextField(blank=True)
    post_date =  models.CharField(max_length=255,blank=True)
    request_count=  models.IntegerField(default=1)
    update_time = models.DateTimeField('events time',blank=True)
    create_time = models.DateTimeField(auto_now=True,blank=True,db_index = True)  # 创建时间(自动获取当前时间)
    verify_time = models.DateTimeField('verify time',blank=True)
    user = models.CharField(max_length=100,blank=True)#对应api的
    uploader = models.CharField(max_length=100,blank=True)#对应api的
    type = models.CharField(max_length=100, blank=True)#以,分割各种类型
    OpenID = models.CharField(max_length=100, blank=True)
    UnionID = models.CharField(max_length=100, blank=True)

    def __unicode__(self): # 将对象以str的方式显示出来
            # 在Python3中使用 def __str__(self):
            return self.url+self.title
