#!/usr/bin/env python
# encoding: utf-8
'''
@author: leexuan
@contact: xuanli19@fudan.edu.cn
@Time : 2019/11/23 上午10:35
@desc: 
'''
import pandas

# with open('../res.csv','r',encoding='utf8') as f :
#     lines = f.readlines()
#     print(lines[:10])
import random
import re
import zlib
import base64
import zlib
import json
import time
import requests
import pymongo


client = pymongo.MongoClient('10.171.6.228',27017)
mydb = client['test']
meituan_comments = mydb['meituan_comments']
header = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
    'Host': 'sh.meituan.com',
    'Referer': 'https://www.meituan.com/meishi/2367201/',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}

query_string ={
    'uuid': 'f948fa88da4c4aebb2e8.1574470856.1.0.0',# f948fa88da4c4aebb2e8.1574470856.1.0.0
    'platform': '1',
    'partner': '126',
    'originUrl': 'https://www.meituan.com/meishi/2367201/',
    'riskLevel': '1',
    'optimusCode': '10',
    'id': '2367201',
    'userId':'',
    'offset': '0',
    'pageSize': '10',
    'sortType': '1'
}

def get_shopID_list():
    pd = pandas.read_csv('../res.csv', encoding='utf8')
    # print(pd[:10])
    # print(pd.loc[:,'id'].values)
    shop_ID = pd.loc[:, 'id'].values
    return list(set(shop_ID))

def scrapy_page_comments_num(shopID):
    request_url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment'
    query_string['uuid']= 'f948fa{}c4aebb2e8.1574470856.1.0.0'.format(random.randint(10000,99999))
    query_string['id'] = shopID
    res = requests.get(request_url , headers=header,params=query_string )
    # print(res.content.decode('utf8'))
    json1 = json.loads(res.content.decode('utf8'))
    return json1['data']['total']
    # print(json1['data']['comments'])

def scrapy_page_comments(shopID):
    nums = scrapy_page_comments_num(shopID)
    pages = nums//10+1
    for page in range(pages):
     try :
        print(f'[{page}]/[{pages}]:')
        request_url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment'
        query_string['uuid']= 'f948fa{}c4aebb2e8.1574470856.1.0.0'.format(random.randint(10000,99999))
        query_string['id'] = shopID
        query_string['offset'] = str(page*10)
        res = requests.get(request_url , headers=header,params=query_string )
        # print(res.content.decode('utf8'))
        json1 = json.loads(res.content.decode('utf8'))
        comments_list = json1['data']['comments']
        for comment in comments_list:
            userid=comment['userId']
            userName = comment['userName']
            comment1 = comment['comment']
            star = comment['star']
            meituan_comments.insert({
                'shopID':str(shopID),
                'userid':str(userid),
                'username':str(userName),
                'comment':str(comment1),
                'star':str(star)
            })
        time.sleep(10*random.random())
     except Exception:
         print('error',shopID)
         time.sleep(100 * random.random())

# os.system('bash ~/tmp/auto_login.sh') 防止断网

if __name__ == '__main__':
    shop_ID_list = get_shopID_list()
    for shop_ID in shop_ID_list:
        print(shop_ID)
        scrapy_page_comments(shop_ID)
        # break
        time.sleep(10*random.random())



