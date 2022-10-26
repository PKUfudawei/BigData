import requests
import time
from fake_useragent import UserAgent
import pandas as pd
import json
import random
import string

ua = UserAgent()
items = []
f = open("fail_list.txt", 'a+')
names = ["id","title","directors","casts","rate"]

for count in range(0,9900,100):
    time.sleep(47+34*random.random())
    headers = {'User-Agent': ua.chrome}
    num = ''.join(random.sample(string.digits + string.ascii_letters, 11))
    cookie = {'bid': num, 'll': '"108296"'}
    res = requests.get('https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&limit=100&tags=%E7%94%B5%E5%BD%B1&start={}'.format(count) ,headers=headers,cookies=cookie)
    print(res.text)
    if res.status_code != 200:
        continue 
    res.encoding = 'utf-8'
    try:
        x = json.loads(res.text)["data"]
    except:
        f.write(str(count)+"\n")
        continue
    if res.status_code == 200:
        print(count)
        for i in x:
            try:
                item = []
                item.append(i["id"])
                item.append(i["title"])
                item.append(",".join(i["directors"]))
                item.append(",".join(i["casts"]))
                item.append(i["rate"])
                items.append(item)
            except:
                continue
    else:
        f.write(str(count)+"\n")

f.close()
result=pd.DataFrame(columns=names,data=items)
result.to_csv('douban.csv',encoding='utf-8')