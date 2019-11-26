#!/usr/bin/env python
# encoding: utf-8
'''
@author: leexuan
@contact: xuanli19@fudan.edu.cn
@Time : 2019/11/22 上午10:22
@desc: 
'''

# import pymongo
#
#
# client = pymongo.MongoClient('10.171.6.228',27017)
# mydb = client['test']
# movietop = mydb['movietop']
# movietop.insert({
#     'name':"我的世界",
#     'price':'42'
# })
import pickle
import re


# def get_locationID_list():
#     with open('location_list.txt', 'r', encoding='utf8') as f:
#         lines = f.readlines()
#         str1 = "".join(lines)
#         patten = re.compile('href="(.*?)">', re.S)
#         res_list = re.findall(patten, str1)
#         location_id_list = [location[:-1].split('b')[-1] for location in res_list]
#         return location_id_list
#
# lis = get_locationID_list()
# print(lis)
import requests
res = requests.get('https://sh.meituan.com/meishi/api/poi/getPoiList?cityName=%E4%B8%8A%E6%B5%B7&cateId=0&areaId=312&sort=&dinnerCountAttrId=&page=1&userId=&uuid=f948fa88da4c4aebb2e8.1574470856.1.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fsh.meituan.com%2Fmeishi%2Fb312%2F&riskLevel=1&optimusCode=10&_token=eJxdjkuvokAUhP9LbyF282xwp%2FJQBOSCiDK5C8VWUJA3qJP579MmdzaTnKTqVH2L%2Bg2a1RlMOYRUhFgwkAZMATdBExmwoGtpI2FRxDLieRWJLEj%2BywTMglOz08D0F8eLPCspyvcn8WlAEwWxCkLf7KcUWIxpyYv0PsyKIiDtuqqdQtimk4JkXX98TJKygNS3aQZPAsdDOgRQvthSnur9R48%2F2v37Hbqcsm12fVBHrPF8C7l6fM%2B%2BUsIEaXySk9jX7ejqt1kd4mU9a7fRxg%2FeVrB2F42k4dyLZxW5lMjdY2K%2FLstdoOeMJsTpbKtrVu2Ee7nXrQWEnsp4gqJny%2BLm7QJSH94hiZz1fDA4t8%2Fnnm9mnH2zyVHoh9o4moMXNDvDKt%2FhKukry9kneZ2aMDey67MXokXzbG4XLYzGBhnP%2BtAM5vkBjTP3iiP5cfcjKF7UCmtLiWkL0ZRG%2B%2FD6Wm9Ecb4pWs%2FiK5dPZQeF915lRrdM9LIEf%2F4C%2FFeOLg%3D%3D'
             ,headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'sh.meituan.com',
    'Referer': 'https://sh.meituan.com/meishi/b666/',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
})
print(res.content.decode('utf8'))

