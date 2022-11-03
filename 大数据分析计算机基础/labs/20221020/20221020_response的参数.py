import requests
import time
import random

headerData={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

try:
	rsps=requests.get(f'https://news.pku.edu.cn/xwzh/de1935030afc4293990075b6a6e5768Z.htm',headers=headerData)
	print("headers=",rsps.headers)
	print("encoding=",rsps.encoding)
	print("status_code=",rsps.status_code)
	print("ok=",rsps.ok)
except Exception as e:
	print(e)