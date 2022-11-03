#单页面抓取，无cookie
import requests
import time
import random

headerData={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

wordList=["mouse","brain","monitor","screen","power"]

for everyWord in wordList:
	rsps=requests.get(f'http://www.iciba.com/word?w={everyWord}',headers=headerData)

	#取得iciba的computer内容,rsps是response的简写


	rsps.encoding="utf-8" #设置网页编码，此处一般为utf-8

	rspsText=rsps.text
	#print("抓取内容输出：",rsps.text) #输出网页文本，rsps.text结果为字符串
	
	webFile=open(f"{everyWord}.html","w",encoding="utf-8")
	webFile.write(rsps.text)
	webFile.close()
	print(f"==========={everyWord}网页已经抓取存储完毕！===============")


	httpPos=rspsText.find("http://res.iciba.com/resource/amp3",0)
	mp3UrlList=[]
	while httpPos!=-1:
		dotMp3Pos=rspsText.find(".mp3",httpPos)
		print(rspsText[httpPos:dotMp3Pos+4])
		mp3UrlList.append(rspsText[httpPos:dotMp3Pos+4])
		httpPos=rspsText.find("http://res.iciba.com/resource/amp3",dotMp3Pos+4)

	for everyURL in mp3UrlList:
		rsps=requests.get(everyURL,headers=headerData)
		if "oxford" in everyURL:
			mp3File=open(f"./England/{everyWord}.mp3","wb")
			mp3File.write(rsps.content)
			mp3File.close()
		else:
			mp3File=open(f"./USA/{everyWord}.mp3","wb")
			mp3File.write(rsps.content)
			mp3File.close()

	print(f"==========={everyWord}的MP3已经抓取存储完毕！===============")

	#设置时间间隔
	waitingSeconds=5+random.randint(1,10)
	print(f"等待中!{waitingSeconds}秒")
	time.sleep(waitingSeconds)#设置时间间隔
	