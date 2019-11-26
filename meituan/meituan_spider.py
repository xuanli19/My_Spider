#!/usr/bin/env python
# encoding: utf-8
'''
@author: leexuan
@contact: xuanli19@fudan.edu.cn
@Time : 2019-11-20 13:30
@desc: meituan_spider
'''
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
meituan = mydb['meituan']
header = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
    'Host': 'sh.meituan.com',
    'Referer': 'https://sh.meituan.com/meishi/b666/',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}

query_string = {
    'cityName': '上海',
    'cateId': '0',
    'areaId': '338',
    'sort': 'sales',
    'dinnerCountAttrId': '',
    'page': '1',
    'userId': '',
    'uuid': 'f948fa88da4c4aebb2e8.1574470856.1.0.0', # 会变化
    'platform': '1',
    'partner': '126',
    'originUrl': 'https://sh.meituan.com/meishi/b666/',
    'riskLevel': '1',
    'optimusCode': '10',
    '_token': 'eJxVjkmPqkAUhf9LbSVSRYEFJr0AHFpFGRSh7fSCUUBoRhF5ef/9lUm/RSc3Oed+59zk/gHNJgRzBKEEIQP6qAFzgKZwOgMM6FqaCITniTDjEUckBgS/GUYCA/zmvADzT8TxHIME+PUiFgWUiJARISWvEDOEiF8Mx9N5dTa0ApKuq9o5y7bJtIjS7u59T4OyYKlvk5T1JcTPWPoJoAfFiR5Qvf2o96Pd/31PX6fdNr1+UxdtH2Fmo/oxymYSTY7JxZ+pH3W20szSsc67cMQypzTv5hNvj7uD2kgLkuiWXEZRyXUuibRn/G4dl/lEMYarkMqtrzu3celyoglP7B2PrFs8UntZXUa/LOLC7o1UewzD2Td0T8bO3VJXsOkvsa2JyIvzXa1lyyzY7G+VJTmCVp/W/XOfH5oMOlWsxmHqs0eVW7mZvnU9YhuIH2wp0KUw4DadI8YTdDCriZHf8BXvFbI2lQGvjVPVLGBYZ2EZKuu6yHEPVf7jsKvktzfw9x/2h49x'
}


def decode_token(token):
    token_decode = base64.b64decode(token)
    token_string = zlib.decompress(token_decode)
    return token_string


def encode_token(token):
    token_string = zlib.compress(token)
    return base64.b64encode(token_string)


def get_locationID_list():
    with open('location_list.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        str1 = "".join(lines)
        patten = re.compile('href="(.*?)">', re.S)
        res_list = re.findall(patten, str1)
        location_id_list = [location[:-1].split('b')[-1] for location in res_list]
        return location_id_list


def scrapy_shop_comments():


    pass


def scrapy_():
    locationID_list =get_locationID_list()
    for locationID in locationID_list:
        try :
            print('scrapy ',locationID,'area')
            pages = scrapy_page_counts(locationID)//14 +1
            print(pages)
            time.sleep(random.random()*100)
            for page in range(pages):
                print(f'{page}/{pages}')
                poi_list = scrapy_page(locationID,page)
                for poi in poi_list:
                    id = poi['poiId']
                    title = poi['title']
                    address =poi['address']
                    avg_price =poi['avgPrice']
                    avgscore=poi['avgScore']
                    meituan.insert({
                        'id': id,
                        'location':locationID,
                        'title':title,
                        'address':address,
                        'avg_price':avg_price,
                        'avgscore':avgscore
                    })

                time.sleep(random.random() * 100)
        except Exception :
            print('scrapy ', locationID, 'area failed')
            time.sleep(random.random()*400)



def scrapy_page(locationID,page):
    request_url = 'https://sh.meituan.com/meishi/api/poi/getPoiList'
    res = decode_token(query_string['_token'])
    json1 = json.loads(res)

    now_time = round(time.time() * 1000)
    next_time = now_time + random.randint(50, 200)
    json1['ts'] = now_time
    json1['cts'] = next_time
    res = (json.dumps(json1)).encode()
    query_string['_token'] = encode_token(res)
    query_string['areaId'] = locationID
    query_string['page'] = str(page + 1)
    res = requests.get(request_url, params=query_string, headers=header)
    json2 = res.content.decode('utf8')
    json2 = json.loads(json2)
    data = json2['data']
    return data['poiInfos']

def scrapy_page_counts(locationID):
    request_url = 'https://sh.meituan.com/meishi/api/poi/getPoiList'
    res = decode_token(query_string['_token'])
    json1 = json.loads(res)

    now_time = round(time.time() * 1000)
    next_time = now_time + random.randint(50, 200)
    json1['ts'] = now_time
    json1['cts'] = next_time
    res = (json.dumps(json1)).encode()
    # print(res)
    query_string['_token'] = encode_token(res)
    query_string['areaId'] = locationID
    res = requests.get(request_url, params=query_string, headers=header)
    json2 = res.content.decode('utf8')
    json2 = json.loads(json2)
    # print(json2)
    data = json2['data']
    return data['totalCounts']

# mongoexport -d test -c movietop -f name,price  --csv -o ~/res.csv 导出数据库成csv的指令

if __name__ == '__main__':
    scrapy_()

# 最大连接异常：requests.exceptions.ConnectionError: HTTPSConnectionPool(host='sh.meituan.com', port=443): Max retries exceeded with url: /meishi/api/poi/getPoiList?cityName=%E4%B8%8A%E6%B5%B7&cateId=0&areaId=35947&sort=sales&dinnerCountAttrId=&page=1&userId=&uuid=7f914b5e4f2640df9a4b.1574247500.1.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fsh.meituan.com%2Fmeishi%2Fb5%2Fsales%2F&riskLevel=1&optimusCode=10&_token=eJyNj8lu4kAURX8FeeuIKhces2vA7rYdAhiwCVEvPOGB9lTlOcq%2Fx4VaiZRVFk8677yrq6o3BusB8zjjIFQgfJgxbYinleHmcC4y014TehUknucVhBaCKE%2FS%2F2YlKEzWw%2FZ60q8c4tHDjJPkv3dpUTdJeaqXIZzk%2F4R0TyCezj2q0yQT13VJHgEg8TwLk7px87lfZGBiEifAQ5IAynwB6ON%2BFEWAoe3ZkbZTun2S%2B0n1l9vQ%2F9N2kkQ55dDogvRUV93462Rdw0NntRUvR73p9cvBjPebhqwuWyJo%2BMQeVHbpVX8kM0SrQx1YMFCVSCbCkmv1XUr8MladQbGsLnwSgPOy5n2w6FmQa2N01QUbu6XajqYN9N9nVAQ29gvL3R8wKzXPGJ21dGxtY8CVsTdEL3UMY392m0wIRkmO%2FLQ3h9bahGx%2FbLz6uF5djSY8wX%2BF7iWiQp52Ttqetec41rxypwxuMCb1BS2ym9%2BJud4PopK5Thj3m2J7sSpH1W5V0fXs9kXFLvP%2BAaxgpbA%3D (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f3f5a86ee48>: Failed to establish a new connection: [Errno 110] Connection timed out',))