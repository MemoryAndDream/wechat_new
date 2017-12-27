# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: testProcess.py 
@time: 2017/12/15 17:30 
"""

from  wechat.crawler.mainprocess import keywordSearch

#re =  keywordSearch('权力的游戏 第二季', sites=[30, 31], sitesType='netDiskSites')['urlinfos']
#for i in re:
#    print i['title']

from  wechat.service.reply_new import pic_reply

pic_reply('http://files.jb51.net/file_images/article/201603/201635144749913.jpg?201625144758')