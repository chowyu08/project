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
import re

reload(sys)
sys.setdefaultencoding('utf8')


class HotelType:
    """docstring for HotelType"""

    def __init__(self, filename):
        self.filename = filename

    def getResult(self):
        try:
            openFileName = './hotel/data/List/' + self.filename
            csvhandler = fileutils.initCsv(
                './hotel/data/Type', self.filename)
            browser = webdriver.Firefox()
            bCrawl = True
            while bCrawl:
                # seed_urls=['http://english.ctrip.com/hotels/shanghai-hotels-list-2/#ctm_ref=ix_pd_n_1','http://english.fat8.qa.nt.ctripcorp.com/hotels/shanghai-hotels-list-2/#ctm_ref=ix_pd_n_1','http://english.fat8.qa.nt.ctripcorp.com/hotels/beijing-hotels-list-1/#ctm_ref=ix_pd_n_2','http://english.fat8.qa.nt.ctripcorp.com/hotels/hong-kong-hotels-list-58/#ctm_ref=ix_pd_n_3','http://english.fat8.qa.nt.ctripcorp.com/hotels/shenzhen-hotels-list-30/#ctm_ref=ix_pd_n_4','http://english.fat8.qa.nt.ctripcorp.com/hotels/chendu-hotels-list-28/#ctm_ref=ix_pd_n_5','http://english.fat8.qa.nt.ctripcorp.com/hotels/sanya-hotels-list-43/#ctm_ref=ix_pd_n_6','http://english.fat8.qa.nt.ctripcorp.com/hotels/guangzhou-hotels-list-32/#ctm_ref=ix_pd_n_8','http://english.fat8.qa.nt.ctripcorp.com/hotels/hangzhou-hotels-list-17/#ctm_ref=ix_pd_n_7','http://english.fat8.qa.nt.ctripcorp.com/hotels/guilin-hotels-list-33/#ctm_ref=ix_pd_n_9','http://english.fat8.qa.nt.ctripcorp.com/hotels/xi-an-hotels-list-10/#ctm_ref=ix_pd_n_10']
                fileHandle = open(openFileName, 'r')
                fileList = fileHandle.readlines()
                nrows = len(fileList)
                index = 0
                for line in fileList:
                    cur_url = line.strip()
                    # cur_url='http://english.fat8.qa.nt.ctripcorp.com/hotels/shanghai-hotel-detail-425161/sport-park-hotel/?city=2&checkin=2016-05-28&checkout=2016-05-29#ctm_ref=lst_n_1_6'
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
                        time.sleep(6)
                        scrollDriver(browser)
                        outputCurrentPageItem(browser, csvhandler)
                        crawl_url = browser.current_url
                        print "%s %s finish crawl, url:%s" % (time.strftime('%Y-%m-%d %H:%M:%S'), index, crawl_url)
                        index += 1
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
        fullFileName = './hotel/data/Type/' + self.filename
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
    #page_src = browser.page_source
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


def get_concrete_hoteltype(hxs):
    try:
        concrete_hoteltype_list = []
        column_pays = hxs.xpath(
            '//table[@class="room_list_table"]//td[@class="column_pay"]')
        for column_pay in column_pays:
            concrete_hoteltype = getcont(column_pay.xpath(
                './/ul[@class="pay_list"]/li/text()').extract()).encode('utf8')
            danbao = getcont(column_pay.xpath(
                './/ul[@class="pay_list"]/li/p/text()').extract()).encode('utf8')
            concrete_hoteltype = concrete_hoteltype + danbao
            concrete_hoteltype_list.append(concrete_hoteltype)
        return concrete_hoteltype_list
    except Exception, e:
        print '[ERROR!]:', str(e)


def get_column_type(hxs):
    try:
        column_type_list = []
        immediate_confirmation_list = []
        column_types = hxs.xpath(
            '//table[@class="room_list_table"]//td[@class="column_type"]')
        for column_type in column_types:
            freeCancel = getcont(column_type.xpath(
                './/div[@class="server_area"]/p/text()').extract()).encode('utf8')
            immediate_confirmation = getcont(column_type.xpath(
                './/div[@class="sum_tip"]/text()').extract()).encode('utf8')
            column_type_list.append(freeCancel)
            immediate_confirmation_list.append(immediate_confirmation)
        return column_type_list, immediate_confirmation_list
    except Exception, e:
        print '[get_column_type_ERROR!]:', str(e)


def get_column_price(hxs):
    try:
        column_price_list = []
        promotion_code_list = []
        column_prices = hxs.xpath(
            '//table[@class="room_list_table"]//td[@class="column_price"]')
        for column_price in column_prices:
            price1 = getcont(column_price.xpath(
                './/a[@class="price"]/dfn/text()').extract()).encode('utf8')
            price2 = getcont(column_price.xpath(
                './/a[@class="price"]/strong/text()').extract()).encode('utf8')
            price = price1 + price2
            promotion_code = getcont(column_price.xpath(
                './/div[@class="sales_box"]/span/text()').extract()).encode('utf8')
            column_price_list.append(price)
            promotion_code_list.append(promotion_code)
        return column_price_list, promotion_code_list
    except Exception, e:
        print '[get_column_price_ERROR!]:', str(e)


def get_column_supply(hxs):
    try:
        freeWifi_list = []
        freeInternet_list = []
        freeBreakfast_list = []
        column_supplys = hxs.xpath(
            '//table[@class="room_list_table"]//td[@class="column_supply"]')
        for column_supply in column_supplys:
            freeWifi = getcont(column_supply.xpath(
                './/span[@class="hotel_ico_box"][1]/i[1]/@title').extract()).encode('utf8')
            freeInternet = getcont(column_supply.xpath(
                './/span[@class="hotel_ico_box"][2]/i[1]/@title').extract()).encode('utf8')
            freeBreakfast = getcont(column_supply.xpath(
                './/span[@class="hotel_ico_box"][3]/i[1]/@title').extract()).encode('utf8')
            freeWifi_list.append(freeWifi)
            freeInternet_list.append(freeInternet)
            freeBreakfast_list.append(freeBreakfast)
        return freeWifi_list, freeInternet_list, freeBreakfast_list
    except Exception, e:
        print '[get_column_supply_ERROR!]:', str(e)


def outputCurrentPageItem(browser, csvhandler):
    try:
        index = 0
        pagesource = browser.page_source
        crawl_url = browser.current_url
        hxs = HtmlXPathSelector(text=pagesource)
        hotel_name = getcont(
            hxs.xpath('//div[@class="tit"]/h1/text()').extract()).encode('utf8')
        infos = hxs.xpath(
            '//table[@class="room_list_table"]//td[@class="column_book"]')
        concrete_hoteltype_list = get_concrete_hoteltype(hxs)
        column_type_list, immediate_confirmation_list = get_column_type(hxs)
        column_price_list, promotion_code_list = get_column_price(hxs)
        freeWifi_list, freeInternet_list, freeBreakfast_list = get_column_supply(
            hxs)
        for info in infos:
            bookHandler = getcont(info.xpath(
                './/button/@onclick').extract()).encode('utf8')
            #book_info="business.bookHandler(690633 12849412 'PP' 0'0''''1''1''0');__SSO_submit();"
            book_info = re.compile('(\d+)\s+(\d+)\s+\'(.*)\'\s+')
            hotel_room_type = re.findall(book_info, bookHandler)
            if len(hotel_room_type):
                hotelid = hotel_room_type[0][0]
                roomid = hotel_room_type[0][1]
                roomtype = hotel_room_type[0][2]
            else:
                hotelid = ''
                roomid = ''
                roomtype = 'Check'
            concrete_hoteltype = concrete_hoteltype_list[index]
            freeCancel = column_type_list[index]
            immediate_confirmation = immediate_confirmation_list[index]
            price = column_price_list[index]
            promotion_code = promotion_code_list[index]
            freeWifi = freeWifi_list[index]
            freeInternet = freeInternet_list[index]
            freeBreakfast = freeBreakfast_list[index]
            index += 1
            # print 'index:', index, 'roomtype:', roomtype, 'concrete_hoteltype:', concrete_hoteltype, 'freeCancel:', freeCancel, 'immediate_confirmation', immediate_confirmation
            data = [crawl_url, hotel_name, hotelid, roomid, roomtype, concrete_hoteltype, freeCancel,
                    immediate_confirmation, price, promotion_code, freeWifi, freeInternet, freeBreakfast, now()]
            fileutils.writeCsv(csvhandler, data)
            time.sleep(0.5)
    except Exception, e:
        print '[outputCurrentPageItem_ERROR!]:', str(e)
