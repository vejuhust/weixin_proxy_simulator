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
import argparse

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



#读取网页结果
def fetch_content(retval):
    if retval.headers.has_key('content-encoding'):
        fileobj = StringIO.StringIO()
        fileobj.write(url.read())
        fileobj.seek(0)
        gzip_file = gzip.GzipFile(fileobj=fileobj)
        content = gzip_file.read()
    else:
        content = retval.read()
    return content



#微信验证请求
def weixin_verify():
    print "[weixin_verify] token='%s'," % token,
    #用GET方法提交验证信息
    request = urllib2.Request(url = generate_url('GET'))
    try:
        time_start = time.time()
        retval = urllib2.urlopen(request, timeout = timeout)
        content = fetch_content(retval)
        time_end = time.time()
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
    #验证结果
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
        content = fetch_content(retval)
        time_end = time.time()
    except urllib2.HTTPError, e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
    #处理结果
    print "response received, %d bytes. it takes %.6f sec." % (len(content), time_end - time_start)
    message_processor(content)



#发送文字消息
def weixin_send_text(filename, content):
    if filename != None:
        try:
            file = open(filename, 'r')
            content = file.read()
            file.close()
        except:
            print "error. can't file %s" % filename
            return
    print "[weixin_send_text] text content\n%s" % content
    print "[weixin_send_text]",
    data = message_text % (openid, int(time.time()), content)
    weixin_send_data(data)



#发送声音消息
def weixin_send_voice():
    print "[weixin_send_voice]",
    data = message_voice % (openid, int(time.time()))
    weixin_send_data(data)



#发送图片消息
def weixin_send_image():
    print "[weixin_send_image]",
    data = message_image % (openid, int(time.time()))
    weixin_send_data(data)



#发送坐标消息
def weixin_send_location():
    print "[weixin_send_location]",
    data = message_location % (openid, int(time.time()))
    weixin_send_data(data)



#主程序
if __name__ == '__main__':
    global url_website
    global token
    global openid
    
    #设置命令行参数
    parser = argparse.ArgumentParser(description='a simulator of weixin message server for developers')
    
    parser.add_argument('--version', action='version', version="%(prog)s 20130315")
    parser.add_argument('-u', '--url', dest = 'url', action = 'store', default = url_website, help = "website to be tested (default in config.py)")
    parser.add_argument('-c', '--check', dest = 'check', action = 'store', default = token, help = "check token (default in config.py)")
    parser.add_argument('-s', '--skip', dest = 'skip', action = 'store_true', default = False, help = "skip message test")
    parser.add_argument('-v', '--voice', dest = 'voice', action = 'store_true', default = False, help = "send voice message")
    parser.add_argument('-i', '--image', dest = 'image', action = 'store_true', default = False, help = "send image message")
    parser.add_argument('-l', '--location', dest = 'location', action = 'store_true', default = False, help = "send location message")
    parser.add_argument('-f', '--file', dest = 'filename', action = 'store', default = None, help = "send text from file")
    parser.add_argument('-t', '--text', dest = 'content', action = 'store', default = "Hello2BizUser", help = "send text directly (default salutatory)")
    parser.add_argument('-o', '--openid', dest = 'openid', action = 'store', default = "oVMe5jjn457qgawhKlXacCAy2bqs", help = "openid in message (default ...)")
    
    #设置全局变量
    args = parser.parse_args()
    url_website = args.url
    token = args.check
    openid = args.openid
    
    #测试过程
    weixin_verify()
    if args.skip == True:
        pass
    elif args.voice == True:
        weixin_send_voice()
    elif args.image == True:
        weixin_send_image()
    elif args.location == True:
        weixin_send_location()
    else:
        weixin_send_text(args.filename, args.content)

