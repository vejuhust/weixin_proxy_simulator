#!/usr/bin/env python
# -*- coding: utf-8 -*-

url_verify = "?signature=%s&timestamp=%s&echostr=%s&nonce=%s"
url_post = "?signature=%s&timestamp=%s&nonce=%s"
echostr = "hello"
headers = { 'Content-Type'  : 'text/xml' }
timeout = 10

#url_website = "http://42.121.3.228/"
url_website = "http://cq01-hao123-rdtest06.vm.baidu.com:8080/weixin_notice"
token = "vej_python_proto"
