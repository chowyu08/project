#!/usr/bin/env python
#encoding=utf-8
import fileutils
import time
import random

All_CRAWLSETS = set(fileutils.readFileUrls('./url/*.txt'))
NO_REMOVE_PROJS = fileutils.getDoneUrls('./*.nremove')

def getCrawlUrl():
    """
    根据days（默认明天），从抓取url链接配置文件中产生一个抓取链接，如果已经抓取过则不再返回
    返回抓取链接模式，本次抓取链接
    链接随机给出
    """
    import re
    already_urlsets = set(fileutils.readFileUrls('./already.urls'))
    crawl_sets = All_CRAWLSETS - already_urlsets
    len_sets = len(crawl_sets) 
    if len_sets >0:
        cur_url= list(crawl_sets).pop(random.randint(0,len_sets-1))
        return  cur_url
    else:
        return None
 
def getCrawlProjectUrl():
    """
    根据days（默认明天），从抓取url链接配置文件中产生一个抓取链接，如果已经抓取过则不再返回
    返回抓取链接模式，本次抓取链接
    链接随机给出
    """
    import re
    all_urlsets = set(fileutils.readUrlsFromCSV('./projects/*.csv'))
    alreadys = NO_REMOVE_PROJS
    alreadys.extend(fileutils.getDoneUrls('./*.projs'))
    alreadys.extend(fileutils.getDoneUrls('./*.ncrawl'))
    already_urlsets = set(alreadys)
    crawl_sets = all_urlsets - already_urlsets
    len_sets = len(crawl_sets) 
    if len_sets >0:
        cur_url= list(crawl_sets).pop(random.randint(0,len_sets-1))
        return  cur_url
    else:
        return None 
 
def getProxy():
    all_proxyset = fileutils.readProxyFile()
    if all_proxyset:
        cur_proxy= list(all_proxyset).pop(random.randint(0,len(all_proxyset)-1))
    else:
        cur_proxy = (None,None)
    return cur_proxy        
    
def storeCrawledUrl(url,file_name='./already.urls'):
    """
    抓取成功，保存本次抓取链接
    """
    fileutils.writeDoneUrls(url,file_name)
    
if __name__ =="__main__":
    print getCrawlUrl()
