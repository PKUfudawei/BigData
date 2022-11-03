#单页面抓取抓取多个网页，无cookie
import requests
import time
import random

#设置Header数据，字典格式，如果没有headerData,将不能得到正确的网页内容
headerData={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

wordList=["computer","brain","mobile","mouse"]
for everyWord in wordList:
	r=requests.get(f'http://www.iciba.com/word?w={everyWord}',headers=headerData) #取得iciba的computer内容
	r.encoding="utf-8" #设置网页编码，此处一般为utf-8
	 
	print("抓取内容输出：",r.text) #输出网页文本，r.text结果为字符串
	 
	webFile=open(f"{everyWord}.html","w",encoding="utf-8")
	webFile.write(r.text)
	webFile.close()
	print("===========",everyWord,"已经抓取完毕！")
	
	waitingSeconds=5+random.randint(1,10)
	print(f"正在等待中……，等待时长为：{waitingSeconds}秒")
	time.sleep(waitingSeconds)