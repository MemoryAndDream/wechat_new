# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: pic_opt.py 
@time: 2017/12/27 17:00 
"""
import os, urllib, uuid
import logging
logger = logging.getLogger('default')
from crawlerTool import crawlerTool as ct
def save_pic(PicUrl,localPath):
    # 本地保存路径
    localPath = localPath
    # 生成一个文件名字符串 
    def generateFileName():
        return str(uuid.uuid1())


    # 根据文件名创建文件 
    def createFileWithFileName(localPathParam, fileName):
        totalPath = localPathParam + '\\' + fileName
        if not os.path.exists(totalPath):
            file = open(totalPath, 'a+')
            file.close()
        return totalPath

    # 根据图片的地址，下载图片并保存在本地 
    def getAndSaveImg(imgUrl):
        if (len(imgUrl) != 0):
            fileName = generateFileName() + '.jpg'

        urllib.urlretrieve(imgUrl, createFileWithFileName(localPath, fileName))


    picPath = getAndSaveImg(PicUrl)
    logger.info('save pic %s' % picPath)

def pic_distinguish_by_url(imgUrl):
    pass
    #tineye.com识别看起来很不错，但是要钱 2毛4一次 贵的一笔
#百度的效果不太好，但是凑合
# #https://image.baidu.com/n/pc_search?queryImageUrl=（url编码后的链接）&fm=index&uptype=urlsearch
    query_url='https://image.baidu.com/n/pc_search?queryImageUrl=%s&fm=index&uptype=urlsearch'%urllib.quote(imgUrl)
    page = ct.getPage(query_url)
    
