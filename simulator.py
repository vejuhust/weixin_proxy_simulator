#!/usr/bin/env python
# -*- coding: utf-8 -*-


from hashlib import sha1
from random import randint
from xml.etree import ElementTree
from message import *
from config import *
import urllib
import urllib2
import json
import StringIO
import gzip
import re
import sys
import time
import random


#解决中文编码问题
reload(sys)
sys.setdefaultencoding( "utf-8" )



#生成URL
def generate_url(method = 'GET'):
    timestamp = str(int(time.time()))
    nonce = str(randint(10000000000,100000000000))
    temp_array = [token, timestamp, nonce]
    temp_array.sort()
    temp_string = ''.join(temp_array)
    signature = sha1(temp_string).hexdigest()
    if method == 'GET':
        url = url_website + url_verify % (signature, timestamp, echostr, nonce)
    elif method == 'POST':
        url = url_website + url_post % (signature, timestamp, nonce)
    return url



#微信验证请求
def weixin_verify():
    print "[weixin_verify]",
    #用GET方法提交验证信息
    request = urllib2.Request(url = generate_url('GET'))
    try:
        time_start = time.time()
        retval = urllib2.urlopen(request, timeout = timeout)
        time_end = time.time()
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
    #解析验证结果
    if retval.headers.has_key('content-encoding'):
        fileobj = StringIO.StringIO()
        fileobj.write(url.read())
        fileobj.seek(0)
        gzip_file = gzip.GzipFile(fileobj=fileobj)
        content = gzip_file.read()
    else:
        content = retval.read()
    if echostr == content:
        print "verified. it takes %.6f sec." % (time_end - time_start)
    else:
        print "wrong ('%s','%s'). it takes %.6f sec." % (echostr, content, time_end - time_start)



#解析反馈XML内容
def message_processor(content):
    print "[message_processor]",
    try:
        root = ElementTree.fromstring(content)
    except:
        print "error, it is not xml.\n%s" % content
        return
    message_type = root.find('MsgType').text
    print message_type
    if message_type == 'text':
        print "~Content~\n", root.find('Content').text
    elif message_type == 'news':
        print "got %s article(s)." % root.find('ArticleCount').text
        items = root.findall('Articles//item')
        item_count = 0
        for  item in items:
            item_count += 1
            print "~[%d]Title~\n" % item_count, item.find('./Title').text
            print "~[%d]Description~\n" % item_count, item.find('./Description').text
            print "~[%d]PicUrl~\n" % item_count, item.find('./PicUrl').text
            print "~[%d]Url~\n" % item_count, item.find('./Url').text



#微信消息请求
def weixin_send_data(data):
    #发送POST请求
    request = urllib2.Request(url = generate_url('POST'), headers = headers, data = data)
    try:
        time_start = time.time()
        retval = urllib2.urlopen(request, timeout = timeout)
        time_end = time.time()
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
    #处理结果
    if retval.headers.has_key('content-encoding'):
        fileobj = StringIO.StringIO()
        fileobj.write(url.read())
        fileobj.seek(0)
        gzip_file = gzip.GzipFile(fileobj=fileobj)
        content = gzip_file.read()
    else:
        content = retval.read()
    print "response received, %d bytes. it takes %.6f sec." % (len(content), time_end - time_start)
    message_processor(content)



#发送文字消息
def weixin_send_text(content = "Hello2BizUser"):
    print "[weixin_send_text]",
    data = message_text % (int(time.time()), content)
    weixin_send_data(data)



#发送声音消息
def weixin_send_voice():
    print "[weixin_send_voice]",
    data = message_voice % int(time.time())
    weixin_send_data(data)



#发送图片消息
def weixin_send_image():
    print "[weixin_send_image]",
    data = message_image % int(time.time())
    weixin_send_data(data)



#发送坐标消息
def weixin_send_location():
    print "[weixin_send_location]",
    data = message_location % int(time.time())
    weixin_send_data(data)



#MAIN
if __name__ == '__main__':
    weixin_verify()
    weixin_send_text("天蝎")
    weixin_send_voice()
    weixin_send_image()
    weixin_send_location()


