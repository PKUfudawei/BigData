import pandas as pd

from lxml import etree
import re
import requests
from fake_useragent import UserAgent
import json
from bs4 import BeautifulSoup

import random
import time

def get_mvdata(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    txt = requests.get(url,headers=headers).text
    xpathmv = etree.HTML(txt)
    #获取数据
    mvdata = {}
    #电影名称
    name = xpathmv.xpath('.//h1/span[1]/text()')[0]
    mvdata['name'] = name
    #评分
    ge = xpathmv.xpath('.//strong[@class="ll rating_num"]/text()')[0]
    mvdata['ge'] = ge
    #评价人数
    number = xpathmv.xpath('.//div[@class="rating_sum"]/a[@class="rating_people"]/span/text()')[0]
    mvdata['number'] =number
    #年份
    year = xpathmv.xpath('.//h1/span[2]/text()')[0][1:5]
    mvdata['year'] = year
    #导演
    director = xpathmv.xpath('.//div[@id="info"]/span[1]/span[@class="attrs"]/a/text()')
    mvdata['director'] = director
    #编剧
    writer = xpathmv.xpath('.//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()')
    mvdata['writer'] = writer
    #主演
    act = xpathmv.xpath('.//div[@id="info"]/span[3]/span[@class="attrs"]/a/text()')
    #时长
    mvdata['act'] = act
    length = xpathmv.xpath('.//span[@property="v:runtime"]/text()')[0]
    mvdata['length'] = length
    soup=BeautifulSoup(txt,"lxml")
    for each in soup.find_all('div',id='info'):
        a=each.text
        tp = re.search(r'类型: (.*)',a)
        if tp==None:
            mvdata['type']= " "
        else:
            mvdata['type']= tp.group(1)
        addr = re.search(r'制片国家/地区: (.*)',a)
        if addr==None:
            mvdata['region']= " "
        else:
            mvdata['region']=addr.group(1)
    return mvdata

temp = pd.read_csv("douban.csv", sep=',', encoding='utf-8')

temp1=temp['id']

PA = []

for i in range(0,9900):
    time.sleep(0.15 + 0.25*random.random())
    try:
        pp = get_mvdata("https://movie.douban.com/subject/{}/".format(temp1[i]))
        print(pp)
    except:
        print('异常')
        continue
    #print(i)
    PA.append(pp)

res = []
names = ['name','ge','number','year','director','writer','act','length','type','region']
for pa in PA:
    mv = []
    for key in names:
        if key == 'director' or key == 'act' or key == 'writer':
            mv.append(",".join(pa[key]))
        elif key == 'type' or key == 'region':
            mv.append(pa[key].replace(' / ',','))
        else:
            mv.append(pa[key])
    res.append(mv)
result=pd.DataFrame(columns=names,data=res)
result.to_csv("douban_mv.csv",encoding='utf-8')