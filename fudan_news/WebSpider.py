#!/usr/bin/env python
# encoding: utf-8
'''
@author: leexuan
@contact: xuanli19@fudan.edu.cn
@Time : 2019-11-19 08:58
@desc: 用于构建校园网搜索引擎.
'''

import re
import requests
import lxml
from lxml import etree
import pickle
header ={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh,zh-CN;q=0.9,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

def req_list(url):
    res = requests.get(url,headers=header)
    return res.content

if __name__ == '__main__':
    url_list_0 = [f'https://news.fudan.edu.cn/xxyw/list{i}.htm' for i in range(1, 252)] #学校要闻
    url_list_1 = [f'https://news.fudan.edu.cn/zhxw/list{i}.htm' for i in range(1, 722)]
    url_list_2 = [f'https://news.fudan.edu.cn/40/list{i}.htm' for i in range(1, 799)]
    url_list_3 = [f'https://news.fudan.edu.cn/64/list{i}.htm' for i in range(1, 675)]
    url_list_4 = [f'https://news.fudan.edu.cn/48/list{i}.htm' for i in range(1, 40)]
    url_list_5 = [f'https://news.fudan.edu.cn/45/list{i}.htm' for i in range(1, 56)] # 通知

    url_list = url_list_0+url_list_1+url_list_2+url_list_3+url_list_4+url_list_5
    All_url_list = []
    print(len(url_list) ) # 2538条网页 ，每个网页大约12条新闻
    print(url_list)
    for url in url_list:
        html = req_list(url).decode('utf8')
        page = etree.HTML(html)
        li_list = page.xpath(u'//li[@class="news i1 clearfix"]')
        for li in li_list:
            url=li.xpath(u'./@data-url')
            if len(url)==1:
                All_url_list.append(url[0])
                print(len(All_url_list),url[0])

    with open('url_list.pkl','wb')as f :
        pickle.dump(All_url_list,f)



