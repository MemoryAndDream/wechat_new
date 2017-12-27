# encoding: utf-8  

""" 
@author: Meng.ZhiHao 
@contact: 312141830@qq.com 
@file: deal_exception.py 
@time: 2017/12/27 15:50 
"""
import time
import logging

logger = logging.getLogger('default')
def my_wrapfunc(func):
    def wrapped_func(*args, **kwargs):
        start = time.time()
        try:
            ret = func(*args, **kwargs)
            logger.debug("%s cost [%s]s, " % (func.__name__, time.time() - start))
            return ret
        except Exception, e:
            logger.error('func [%s] error [%s]'%(func.__name__,str(e)))
    return wrapped_func