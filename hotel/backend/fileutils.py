#!/usr/bin/env python
# encoding=utf-8
import csv
import time
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def readFileUrls(file_patten='./url/*.txt'):
    """
    读取url内容，返回list
    """
    from glob import glob
    file_names = glob(file_patten)
    urls = []
    for file_name in file_names:            
        lines = open(file_name).readlines()  # 打开文件，读入每一行
        for line in lines:
            if line.startswith('http'):
                urls.append(line.strip())    
    return urls


def readUrlsFromCSV(file_patten='./hotellist/hotellist_urls.csv', ret_col=[5], check_col=0):
    from glob import glob
    file_names = glob(file_patten)
    urls = []
    for file_name in file_names:
        reader = csv.reader(file(file_name, 'rb'))
        for line in reader:
            item = ''
            for column in ret_col:
                item += line[column] + ","
            if check_col > -1:
                if line[check_col].startswith('http'):
                    urls.append(item[:-1].strip()) 
            else:
                urls.append(item[:-1].strip())                            
    return urls


def readProxyFile(file_patten='./url/proxy*.ini'):
    """
    读取文件
    """
    from glob import glob
    import re
    file_names = glob(file_patten)
    proxys = []
    for file_name in file_names:            
        lines = open(file_name).readlines()  # 打开文件，读入每一行
        for line in lines:
            matches = re.findall(
                r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(\d{2,5})''', line, re.VERBOSE)  
            if matches:
                tuple_ip = (matches[0][0], matches[0][1])
                proxys.append(tuple_ip)    
    return proxys    


def readTemplate(check_sets, file_patten='./url/*.template', checkcolumnsize=2):
    """
    读取Template(内容，返回list
    """
    from glob import glob
    import re
    file_names = glob(file_patten)
    fomat_rets = []
    for file_name in file_names:            
        lines = open(file_name).readlines()  # 打开文件，读入每一行
        for line in lines:
            split_items = re.findall('(\S+)[\s]*', line.strip())
            if len(split_items) == 1:
                split_items = line.strip().split('-')
                if len(split_items) >= 2:
                    if split_items[0].decode('gbk') in check_sets and split_items[1].decode('gbk') in check_sets:
                        fomat_rets.append(split_items[:2])   
                    else:
                        print split_items[0], "->", split_items[1] 
    return fomat_rets


def writeDoneUrls(urls, file_name='./already.urls'):
    """
    读取url内容，返回list
    """
    try:
        hfile = file(file_name, 'a')
        hfile.writelines(urls)
        hfile.close()
    except IOError, ex:
        print ex
        return False
    return True


def getDoneUrls(file_patten='./already.urls'):
    from glob import glob
    urls = []      
    file_names = glob(file_patten)
    for file_name in file_names:            
        lines = open(file_name).readlines()  # 打开文件，读入每一行
        for s in lines:
            if s:
                surl = s.split(',')[0]
                urls.append(surl)
    return urls


def initCsv(path, csvname='', byday=False, append=False):
    """
    Init csv
    """
    # print sys.path[0]
    try:
        if path:
            filename = path
        if csvname:
            filename = os.path.join(filename, csvname)
        elif byday:
            filename = os.path.join(filename, time.strftime("%Y%m%d") + '.csv')
        else:
            filename = os.path.join(
                filename, time.strftime("%Y%m%d%H%M%S") + '.csv')
        if append:
            mode = 'ab+'
        else:
            mode = 'wb'
        csvfile = file(filename, mode)
        return csvfile    
    except Exception, ex:
        print "new file error: ", ex        


def writeCsv(csvfile, content_list, trans_code=True, en_code="GB18030"):
    # print csvfile
    if csvfile:
        try:
            writer = csv.writer(csvfile)
            if trans_code:
                writer.writerow([content.replace(u'\n', '').encode(
                    en_code) for content in content_list])
            else:
                writer.writerow(content_list)
            csvfile.flush()    
        except IOError, ex:
            print "write err:", ex          
    else:
        print "No found csv file handler."


def closeCsv(csvfile):
    """
    Close Csv
    """
    csvfile.close()        


if __name__ == '__main__':
    readUrlsFromCSV()
