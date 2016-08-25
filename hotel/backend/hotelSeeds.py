#!/usr/bin/env python
# encoding=utf-8
import csv
import time
import os
import sys
import fileutils
import datetime
import random

reload(sys)
sys.setdefaultencoding('utf8')


class HotelSeeds:
    """docstring for HotelSeeds"""

    def __init__(self, env, site, city):
        self.env = env
        self.site = site
        self.city = city

    def newFileName(self):
        return self.env + "_" + self.site + "_" + self.city + "_" + str(datetime.date.today())[5:7] \
            + str(datetime.date.today())[8:10] + "_" + \
            str(random.randint(10000, 99999)) + ".csv"

    def get_seeds_url(self):
        page = 'list'
        language = 'HK'
        cities = {'beijing': '1', 'shanghai': '2',
                  'hong-kong': '58', 'sanya': '43', 'guangzhou': '32'}
        filename = self.newFileName()
        csvhandler = fileutils.initCsv('./hotel/data/Seed', filename)
        site_name = self.site
        city_name = self.city
        try:
            # city_id=cities.values()
            if self.env == 'online':
                if (site_name == 'english') or (site_name == 'jp') or (site_name == 'fr') or (site_name == 'es') or (site_name == 'ru') or (site_name == 'de'):
                    # for city_name in city_names:
                    seed_url = 'http://' + site_name + '.' + 'ctrip.com/hotels/' + city_name\
                        + '-hotels-' + page + '-' + cities.get(city_name) + '/'
                    seed_url1 = 'http://' + site_name + '.' + 'ctrip.com/hotels/' + city_name\
                        + '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=2'
                    seed_url2 = 'http://' + site_name + '.' + 'ctrip.com/hotels/' + city_name\
                        + '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=3'
                    # print seed_url, seed_url1, seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
                elif (site_name == 'hk'):
                    # for city_name in city_names:
                    # http://www.fat8.qa.nt.ctripcorp.com.hk/hotels/shanghai-hotels-list-2/?curr=HKD&language=HK
                    # http://www.fat8.qa.nt.ctripcorp.com.hk/hotels/shanghai-hotels-list-2/?curr=HKD&language=EN
                    seed_url = 'http://www.' + 'ctrip.com.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + \
                        '?curr=HKD&language=' + language
                    seed_url1 = 'http://www.' + 'ctrip.com.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + \
                        '?curr=HKD&language=' + language + '&pageno=2'
                    seed_url2 = 'http://www.' + 'ctrip.com.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + \
                        '?curr=HKD&language=' + language + '&pageno=3'
                    # print seed_url, seed_url1, seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
                elif (site_name == 'sg') or (site_name == 'my'):
                    # for city_name in city_names:
                    seed_url = 'http://www.' + 'ctrip.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + cities.get(city_name) + '/'
                    seed_url1 = 'http://www.' + 'ctrip.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=2'
                    seed_url2 = 'http://www.' + 'ctrip.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=3'
                    # print seed_url, seed_url1, seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
                else:
                    # for city_name in city_names:
                    seed_url = 'http://www.' + 'ctrip.co.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + cities.get(city_name) + '/'
                    seed_url1 = 'http://www.' + 'ctrip.co.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=2'
                    seed_url2 = 'http://www.' + 'ctrip.co.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=3'
                    # print seed_url, seed_url1, seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
            elif self.env == 'fat8':
                test_enviroment = self.env
                if (site_name == 'english') or (site_name == 'jp') or (site_name == 'fr') or (site_name == 'es') or (site_name == 'ru') or (site_name == 'de'):
                    seed_url = 'http://' + site_name + '.' + test_enviroment + '.qa.nt.ctripcorp.com/hotels/' + city_name\
                        + '-hotels-' + page + '-' + cities.get(city_name) + '/'
                    seed_url1 = 'http://' + site_name + '.' + test_enviroment + '.qa.nt.ctripcorp.com/hotels/' + city_name\
                        + '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=2'
                    seed_url2 = 'http://' + site_name + '.' + test_enviroment + '.qa.nt.ctripcorp.com/hotels/' + city_name\
                        + '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=3'
                    # print seed_url,seed_url1,seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
                elif (site_name == 'hk'):
                    seed_url = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.com.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + \
                        '?curr=HKD&language=' + language
                    seed_url1 = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.com.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + \
                        '?curr=HKD&language=' + language + '&pageno=2'
                    seed_url2 = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.com.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + \
                        '?curr=HKD&language=' + language + '&pageno=3'
                    # print seed_url,seed_url1,seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
                elif (site_name == 'sg') or (site_name == 'my'):
                    seed_url = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + cities.get(city_name) + '/'
                    seed_url1 = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=2'
                    seed_url2 = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=3'
                    # print seed_url,seed_url1,seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
                else:
                    seed_url = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.co.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + cities.get(city_name) + '/'
                    seed_url1 = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.co.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=2'
                    seed_url2 = 'http://www.' + test_enviroment + '.qa.nt.ctripcorp.co.' + site_name + '/hotels/' + city_name +\
                        '-hotels-' + page + '-' + \
                        cities.get(city_name) + '/' + '?pageno=3'
                    # print seed_url,seed_url1,seed_url2
                    data = [seed_url]
                    fileutils.writeCsv(csvhandler, data)
                    data1 = [seed_url1]
                    fileutils.writeCsv(csvhandler, data1)
                    data2 = [seed_url2]
                    fileutils.writeCsv(csvhandler, data2)
        except Exception, e:
            print '[get_seeds_url-ERROR]:', str(e)
        result = {}
        fullFileName = './hotel/data/Seed/' + filename
        # print fullFileName
        if self.fileExits(fullFileName):
            result['filename'] = fullFileName
            # print 'file exits *******'
        else:
            result['filename'] = 'false'
            # print 'file not exits -----'
        return result

    def fileExits(self, filename):
        return os.path.exists(filename)

if(__name__ == '__main__'):
    print ''
