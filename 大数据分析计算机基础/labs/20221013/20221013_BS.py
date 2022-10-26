#字符串方法分析网页

from bs4 import BeautifulSoup #第三方库

htmlFile=open("www.pku.edu.cn.html","r",encoding="utf-8")
htmlContent=htmlFile.read()
htmlFile.close()

oBS=BeautifulSoup(htmlContent,"html.parser")
print(oBS.a)
print(oBS.img)

hrefs=oBS.find_all("a")#找到所有的a元素
for everyHref in hrefs:
	linkText,linkHref=everyHref.get_text(),everyHref.attrs.get("href","")
	if "http" not in linkHref:
		linkHref="https://www.pku.edu.cn"+linkHref
	print(f"{linkText}====>{linkHref}")

imgs=oBS.find_all("img")#找到所有的a元素
for everyImg in imgs:
	print(everyImg)

print(oBS.body.get_text())