#!D:\Python27\python.exe
# -*- coding: UTF-8 -*-   

print "Content-type:text/html"
print  

import MySQLdb
import re
import urllib
import urllib2
class News:
     #构造函数
    def __init__(self):
        self.url = "http://news.baidu.com/"
      #去除包含div
    def tranTags(self, x):
        pattern = re.compile('<div.*?</div>')
        res = re.sub(pattern, '', x)
        return res
      #getpage
    def getPage(self):
        url = self.url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()
       #getnavcode 
    def getNavCode(self):
        page = self.getPage()
        pattern = re.compile('(<ul class="clearfix".*?)<i class="slogan"></i>', re.S)
        navCode = re.search(pattern, page)
        return navCode.group(1)
        #getnav
    def getNav(self):
        navCode = self.getNavCode()
        pattern = re.compile('<a href="(http://.*?)/.*?>(.*?)</a>', re.S)
        items = re.findall(pattern, navCode)
        return items
        #getcontent
    def getContent(self):
        page = self.getPage()
        Middle=re.compile('(<div class="hotnews" alog-group="focustop-hotnews".*?)<div class="column clearfix" id="tupianxinwen">',re.S)
        content = re.search(Middle, page)
        return content.group(1)
        #getMiddle
    def getMiddle(self):
        content=self.getContent()
        #print content 
        pattern=re.compile('<a href="(http://.*?)".*?>(.*?)</a>',re.S)
        items=re.findall(pattern,content)
        return items  
# 打开数据库连接
db = MySQLdb.connect("localhost","root","root","shixun",charset="GBK") 

# 使用cursor()方法获取操作游标   
cursor = db.cursor()
#实例化类
news = News()
items = news.getMiddle() 
for item in items:
    print item[0],news.tranTags(item[1])
    vall = news.tranTags(item[1])
    # SQL 插入语句
    sql = """INSERT INTO two(title,url)VALUES (%s, %s)""" %("'"+vall+"'","'"+item[0]+"'")   
    try:
          # 执行sql语句
        cursor.execute(sql)
          # 提交到数据库执行
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()

    