import requests
import re
import csv
import urllib.request
from lxml import etree
#定义爬虫的请求头header
header={
        'User-Agent': 'Mozilla/5.0 ',
        'Host':'fullsearch.cnepaper.com'
        }
def getpage(key):#得到网页的总页数
    url='http://fullsearch.cnepaper.com/eso/zhtqb.aspx?__VIEWSTATE=%2FwEPDwULLTE4NTgxMDgzMjQPZBYCAgEPZBYCAgMPDxYEHgtSZWNvcmRjb3VudAJ2HhBDdXJyZW50UGFnZUluZGV4AgJkZGQ6U13G0PL%2B1VJSEG6AGa95L6QI2g%3D%3D&__VIEWSTATEGENERATOR=89AA0733&__EVENTTARGET=AspNetPager1&__EVENTARGUMENT=1&__EVENTVALIDATION=%2FwEWBQL%2F9Zz%2FAgKMwc%2FlAQK2hea3DQL4p5WKCgLY0YCrAfGXCBjr9TO8dnRwOyJD%2FObR9hIh&search_text='+key+'&Txt_SiteStart=2016-07-27&Txt_SiteEnd=2020-07-27&AspNetPager1_input=2&lblPaperID=2970'
    res=requests.get(url,headers=header).text
    #print(res)
    pagecon=re.findall('下一页</a><a href="(.*?)" style="margin-right:5px;">末页',res)[0]
    page=re.findall('[0-9]{2}',pagecon)[0]
    return int(page)
def gethtml(pg,key):#得到网页源码
    url='http://fullsearch.cnepaper.com/eso/zhtqb.aspx?__VIEWSTATE=%2FwEPDwULLTE4NTgxMDgzMjQPZBYCAgEPZBYCAgMPDxYEHgtSZWNvcmRjb3VudAJ2HhBDdXJyZW50UGFnZUluZGV4AgJkZGQ6U13G0PL%2B1VJSEG6AGa95L6QI2g%3D%3D&__VIEWSTATEGENERATOR=89AA0733&__EVENTTARGET=AspNetPager1&__EVENTARGUMENT='+str(pg)+'&__EVENTVALIDATION=%2FwEWBQL%2F9Zz%2FAgKMwc%2FlAQK2hea3DQL4p5WKCgLY0YCrAfGXCBjr9TO8dnRwOyJD%2FObR9hIh&search_text='+key+'&Txt_SiteStart=2016-07-27&Txt_SiteEnd=2020-07-27&AspNetPager1_input=2&lblPaperID=2970'
    reshtml=requests.get(url,headers=header).text
    return reshtml
def writenew(csvwriter,reshtml):#写进csv表格
    treedata=etree.HTML(reshtml)
    news=treedata.xpath('//*[@id="need"]/li')
    for each in news:
        title=each.xpath('.//span/a/text()')[0]
        link=each.xpath('.//span/a/@href')[0]
        content1=each.xpath('.//p[1]')[0]
        content = content1.xpath('string(.)')
        dateauthor=each.xpath('//p[2]/text()')[0]
        date=re.findall('日期:(.*)',dateauthor.strip())[0]
        author=re.findall('作者:(.*)',dateauthor.strip())[0]
        print(title)
        print(link)
        print(content)
        print(date)
        print(author)
        csvwriter.writerow([title,link,author.strip(),date.strip(),content.strip()])
def main():
    keyword=input('输入关键词：')
    key=urllib.request.quote(keyword)
    with open(keyword+'.csv','a',newline='',encoding='gb18030')as f:
        csvwriter=csv.writer(f,dialect='excel')
        csvwriter.writerow(['标题','网址','作者','日期','简介'])
        page=getpage(key)
        for pg in range(1,page+1):
            reshtml=gethtml(pg,key)
            writenew(csvwriter,reshtml)
if __name__=="__main__":
    main()