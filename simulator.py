#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
import StringIO
import gzip
import re
import sys
import time
import httplib


#解决中文编码问题
reload(sys)
sys.setdefaultencoding( "utf-8" )


#网页相关
#url_post = "http://42.121.3.228/?signature=5bbce5b6be9bb5695b1b9219c49c92a7ada094f4&timestamp=1357882995&nonce=1357161369"
url_post = "http://42.121.3.228/?signature=9073713b089fbea61c65ddc3dad48f5c1a0a71fe&timestamp=1357895461&nonce=1357662087"
#url_post = "http://cq01-hao123-rdtest06.vm.baidu.com:8080/weixin_notice"
timeout = 10

url_get = "http://42.121.3.228/?signature=5bbce5b6be9bb5695b1b9219c49c92a7ada094f4&timestamp=1357882995&echostr=get_check_ok&nonce=1357161369"
headers = {
    'Content-Type'  : 'text/xml',
}


#获取POST原始页面
def fetch_post_content(post_data):
    request = urllib2.Request(url = url_post, headers = headers, data = post_data)
    while True:
        try:
            retval = urllib2.urlopen(request, timeout = timeout)
        except urllib2.HTTPError, e:
            print e
            exit()
        except urllib2.URLError, e:
            print e
            exit()
        else:
            break
    if retval.headers.has_key('content-encoding'):
        fileobj = StringIO.StringIO()
        fileobj.write(url.read())
        fileobj.seek(0)
        gzip_file = gzip.GzipFile(fileobj=fileobj)
        content = gzip_file.read()
    else:
        content = retval.read()
    return content


#获取GET原始页面
def fetch_get_content():
    request = urllib2.Request(url = url_get)
    while True:
        try:
            retval = urllib2.urlopen(request, timeout = timeout)
        except urllib2.HTTPError, e:
            print e
            exit()
        except urllib2.URLError, e:
            print e
            exit()
        else:
            break
    if retval.headers.has_key('content-encoding'):
        fileobj = StringIO.StringIO()
        fileobj.write(url.read())
        fileobj.seek(0)
        gzip_file = gzip.GzipFile(fileobj=fileobj)
        content = gzip_file.read()
    else:
        content = retval.read()
    return content


#读入post原始数据
def read_post_content(filename):
    post_file = open(filename)
    content = post_file.read()
    post_file.close()
    return content

#MAIN
if __name__ == '__main__':
    post_data = read_post_content("msg3.txt")
    print fetch_get_content()
    print fetch_post_content(post_data)

