#!/usr/bin/env python
# encoding: utf-8
'''
@author: leexuan
@contact: xuanli19@fudan.edu.cn
@Time : 2019-11-20 15:29
@desc: 校园网页的解析  time,title,content,
'''
# TODO
import re
import requests
import lxml
from lxml import etree
import pickle
import csv

def get_url_list():
    res = None
    with open('url_list.pkl','rb') as f :
        res = pickle.load(f)
    return res

csvFile = open("result1.csv", "w+",newline='')
writer = csv.writer(csvFile,delimiter='#')



def get_contents(url):
    if not url.endswith(".htm"):
        return
    # url ='/2019/1119/c4a103063/page.htm'
    new_url = 'https://news.fudan.edu.cn'+url
    res = requests.get(new_url)
    try:
        if res.status_code==200:
            res_content = res.content
            tree = etree.HTML(res_content.decode('utf8'))
            title = tree.xpath(u'//h1[@class="arti_title"]/text()')[0]
            publish_time  =tree.xpath(u'//span[@class="arti_update"]/text()')[0]
            contents = tree.xpath(u'//p/text()')
            # print(new_url)
            # print(title)
            # print(str(publish_time).split('：')[-1] )
            # print("".join(contents).replace('#',','))
            # print()
            li = [new_url,title,str(publish_time).split('：')[-1],"".join(contents).replace('#',',')]
            writer.writerow(li)
    except Exception:
        return


if __name__ == '__main__':
    url_list = get_url_list()

    for i,url in enumerate(url_list):
        get_contents(url)
        print(i,url)
        # break
    csvFile.close()

