#!/usr/bin/env python
# encoding=utf-8
import csv
import time
import os
import sys
from scrapy.selector import HtmlXPathSelector
import requests
import fileutils
from selenium import webdriver
import urlutils
import re
import xlrd

reload(sys)
sys.setdefaultencoding('utf8')


class HotelList:
    """docstring for ClassName"""

    def __init__(self, filename):
        self.filename = filename
        print self.filename

    def getList(self):
        try:
            openFileName = './hotel/data/Seed/' + self.filename
            csvhandler = fileutils.initCsv(
                './hotel/data/List', self.filename)
            browser = webdriver.Firefox()
            bCrawl = True
            while bCrawl:
                fileHandle = open(openFileName, 'r')
                fileList = fileHandle.readlines()
                nrows = len(fileList)
                index = 0
                for line in fileList:
                    cur_url = line.strip()
                    # cur_url='http://english.fat8.qa.nt.ctripcorp.com/hotels/beijing-hotels-list-1/#ctm_ref=ix_pd_n_2'
                    print "%s begin crawl %s" % (time.strftime('%Y-%m-%d %H:%M:%S'), cur_url)
                    try:
                        browser.title
                    except:
                        break
                    browser.implicitly_wait(5)
                    browser.get(cur_url)
                    checkOk = checkLoadOk(browser)
                    while checkOk < 1 and bRefreshTimes < 5:
                        time.sleep(random.randint(2, 5))
                        bRefreshTimes += 1
                        checkOk = checkLoadOk(browser)
                    else:
                        browser.stop_client()
                    try:
                        cur_page = 1
                        time.sleep(6)
                        scrollDriver(browser)
                        #pageul = browser.find_element_by_xpath("//div[@class='pager']")
                        #nextli = pageul.find_elements_by_xpath(".//a[@class='page_next']")
                        outputCurrentPageItem(browser, csvhandler)
                        crawl_url = browser.current_url
                        index += 1
                        print "%s %s finish crawl, url:%s" % (time.strftime('%Y-%m-%d %H:%M:%S'), index, crawl_url)
                    except Exception, ex:
                        print ex.message
                    if index == nrows:
                        break
                if index == nrows:
                    break
            fileutils.closeCsv(csvhandler)
            browser.close()
        except Exception, ex:
            print ex.message
        result = {}
        fullFileName = './hotel/data/List/' + self.filename
        # print fullFileName
        if self.fileExits(fullFileName):
            result['filename'] = self.filename
            # print 'file exits *******'
        else:
            result['filename'] = 'false'
            # print 'file not exits -----'
        return result

    def fileExits(self, filename):
        return os.path.exists(filename)


def get_pagesource(url, trytimes=5):
    try:
        for i in xrange(trytimes):
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                time.sleep(10)
                hxs = HtmlXPathSelector(text=r.content)
                return hxs
            else:
                time.sleep(0.5)
    except:
        print "Try times: %s ,url:%s" % (i, url)
        time.sleep(0.5)


def getcont(tab):
    if tab == []:
        return ''
    else:
        result = ''
        for item in tab:
            result = result + item.strip()
        return result.replace(',', '').replace('\n', '').replace('\r', '')


def now():
    t = time.strftime('%Y-%m-%d %X', time.localtime())
    return t


def checkVerifyCode(browser, wait=120):
    page_src = browser.page_source
    page_url = browser.current_url
    if 'busy' in page_url:
        time.sleep(wait)
        return 0
    return 1


def checkLoadOk(browser):
    return checkVerifyCode(browser)


def scrollDriver(browser):
    browser.execute_script(""" 
                        (function () { 
                        var y = 0; 
                        var step = 200; 
                        window.scroll(0, 0); 

                        function f() { 
                        if (y < document.body.scrollHeight) { 
                        y += step; 
                        window.scroll(0, y); 
                        setTimeout(f, 500); 
                        } else { 
                        window.scroll(0, 0); 
                        document.title += "scroll-done"; 
                        } 
                        } 

                        setTimeout(f, 2000); 
                        })(); 
                        """)
    for i in xrange(240):
        if "scroll-done" in browser.title:
            # reset title
            browser.execute_script(""" 
                         (function () {                          
                         document.title="org:"
                         })(); 
                        """)
            break
        time.sleep(0.5)


def outputCurrentPageItem(browser, csvhandler):
    try:
        index = 0
        pagesource = browser.page_source
        crawl_url = browser.current_url
        hxs = HtmlXPathSelector(text=pagesource)
        infos = hxs.xpath('//div[@class="hotel_info"]/h3[@class="hotel_name"]')
        for info in infos:
            hotel_url = getcont(info.xpath(
                './/a/@href').extract()).encode('utf8')
            index += 1
            # print 'index:', index, 'hotel_url:', hotel_url
            # http://english.fat8.qa.nt.ctripcorp.com/hotels/beijing-hotel-detail-436894/piao-home-inn-wangfujing/?city=1&checkin=2016-06-23&checkout=2016-06-24&label=rucYHjrmdkubWIwnwpRQFQ&salestype=0&page=3&position=4&minprice=155#ctm_ref=lst_n_3_4
            hotel_id = u1 = hotel_url.split(
                '/')[4].split('-')[3].encode('utf8')
            data = [hotel_url, hotel_id]
            fileutils.writeCsv(csvhandler, data)
    except Exception, e:
        print '[ERROR!]:', str(e)
# try:
# 	#can modify the sava path: E:\hote_room_type\hotellist\hotellist_urls.csv
# 	csvhandler = fileutils.initCsv('./hotellist','hotellist_urls.csv')
# 	browser = webdriver.Firefox()
# 	bCrawl = True
# 	while bCrawl:
# 		fileHandle=open(".\hotelSeedsUrl\seeds_url.csv",'r')
# 		fileList=fileHandle.readlines()
# 		nrows=len(fileList)
# 		index = 0
# 		for line in fileList:
# 			cur_url=line.strip()
# 			#cur_url='http://english.fat8.qa.nt.ctripcorp.com/hotels/beijing-hotels-list-1/#ctm_ref=ix_pd_n_2'
# 			print "%s begin crawl %s"%(time.strftime('%Y-%m-%d %H:%M:%S'),cur_url)
# 			try:
# 				browser.title
# 			except:
# 				break
# 			browser.implicitly_wait(5)
# 			browser.get(cur_url)
# 			checkOk = checkLoadOk(browser)
# 			while checkOk < 1  and bRefreshTimes<5:
# 				time.sleep(random.randint(2,5))
# 				bRefreshTimes += 1
# 				checkOk = checkLoadOk(browser)
# 			else:
# 				browser.stop_client()
# 			try:
# 				cur_page = 1
# 				time.sleep(6)
# 				scrollDriver(browser)
# 				#pageul = browser.find_element_by_xpath("//div[@class='pager']")
# 				#nextli = pageul.find_elements_by_xpath(".//a[@class='page_next']")
# 				outputCurrentPageItem(browser)
# 				crawl_url=browser.current_url
# 				index += 1
# 				print "%s %s finish crawl, url:%s"%(time.strftime('%Y-%m-%d %H:%M:%S'),index,crawl_url)
# 			except Exception, ex:
# 				print ex.message
# 			if index==nrows:
# 				break
# 		if index==nrows:
# 			break
# 	fileutils.closeCsv(csvhandler)
# 	browser.close()
# except Exception, ex:
# 	print ex.message
