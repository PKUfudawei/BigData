#分析上证指数网页
import requests
from bs4 import BeautifulSoup
import time
import random

"""
rFile=open("szIndex_202202.html","r",encoding="utf-8")
szData=rFile.read()
rFile.close()

print(szData[:100])
"""

def getDataFromWebPage(htmlCode):
	oBS=BeautifulSoup(htmlCode,"html.parser")
	Tables=oBS.select("table.table_bg001")#找到所有的table元素
	print(f"有Table{len(Tables)}个")
	allData=[]#保存所有数据
	for everyRow in Tables[0].find_all("tr"):
		allTds=everyRow.find_all("td")
		rowData=[]
		for everyTd in allTds:
			rowData.append(everyTd.text.replace(",",""))
		allData.append(tuple(rowData))
	return allData

headerData={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
for stockYear in range(2016,2020+1):
	for Season in range(1,4+1):
		paraData={"year":stockYear,"season":Season}
		dataUrl=f'http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html'
		print(dataUrl)
		rsps=requests.get(dataUrl,headers=headerData,params=paraData)
		rsps.encoding="utf-8" #设置网页编码，此处一般为utf-8
		rspsText=rsps.text
		seasonData=getDataFromWebPage(rspsText)
		print(seasonData)

		print(f"===={stockYear}年{Season}季度的数据处理完毕！===")

		#设置时间间隔
		waitingSeconds=5+random.randint(1,10)
		print(f"等待中!{waitingSeconds}秒")
		time.sleep(waitingSeconds)#设置时间间隔
