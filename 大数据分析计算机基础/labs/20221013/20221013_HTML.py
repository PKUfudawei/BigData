#字符串方法分析网页

htmlFile=open("www.pku.edu.cn.html","r",encoding="utf-8")
htmlContent=htmlFile.read()
htmlFile.close()

print(htmlContent[:100])

linkList=[]
startPos=0
while True:
	startPos=htmlContent.find("<a",startPos)
	
	if startPos==-1:
		break #停止循环

	if startPos!=-1:
		endPos=htmlContent.find("</a>",startPos)
		#startPos指定查找的起点，如果不指定，则从编号0开始，指定则从指定位置开始
	
	linkList.append(htmlContent[startPos:endPos+4])

	startPos=endPos+4

print(linkList[:10])
newLinkList=[link for link in linkList if "href" in link if "javascript" not in link]
print(newLinkList[:10])

finalLink=[]
for everyLink in newLinkList:
	startPos=everyLink.find("href=")
	endPos=everyLink.find(">",startPos)
	href=everyLink[startPos+6:endPos]
	quotePos=href.find('\"')#查找双引号的位置
	if quotePos!=-1:
		href=href[:quotePos]
	if "http" not in href:
		href="https://www.pku.edu.cn"+href
	print(href)
	finalLink.append(href)

print("北大首页链接的数量：",len(finalLink))

print([x for x in finalLink if "pku" not in x])