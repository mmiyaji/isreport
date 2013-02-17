#!/usr/bin/ python
# -*- coding: utf-8 -*-
import cookielib
import commands
from cookielib import CookieJar, DefaultCookiePolicy
import urllib,urllib2,sys,re
import time
import datetime

# クッキーの設定
policy = cookielib.DefaultCookiePolicy(
		rfc2965=True, strict_ns_domain=DefaultCookiePolicy.DomainStrict,
		)
# クッキーオブジェクトの作成
cj = cookielib.CookieJar(policy)
# HTTPCookieProcessorにクッキーの処理を任せる。
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# 引数でパース先を決める
argvs = sys.argv
index = argvs[1]
# index = "/Users/mmiyaji/tmp/reports/isdlreport/2009/0610/008/report20090610008.html"
commands.getoutput('echo "input:'+index+'" >> script_result_author2.txt')
p = index.split("/")
pp = ""
for i in range(len(p)-1):
	print p[i]
	pp +=p[i]+"/"
print pp
path = index.replace("/index.html","")
# .lastIndexOf("1");
# allLines = open('/Users/mmiyaji/tmp/reports/isdlreport/2009/0610/002/report20090610002.html').read()
# allLines = open('/Users/mmiyaji/MJ/2010/program/django/isapps/isbooks/isbookshelf/templates/isbookshelf/isdl_sample.html').read()
allLines = open(index).read()
# head, body = allLines.split('<div class="body">')
try:
	head, body = allLines.split('<body>')
	h,ti1 = head.split('<title>')
	title,ti2 = ti1.split('</title>')
	meat, tail = body.split('</body>')
except:
	head, body = allLines.split('<BODY>')
	h,ti1 = head.split('<TITLE>')
	title,ti2 = ti1.split('</TITLE>')
	meat, tail = body.split('</BODY>')
	
meat = meat.replace('<meta name="GENERATOR" content="TtH 3.80">','')
meat = meat.replace('<meta name="GENERATOR" content="TtH 3.87">','')
meat = meat.replace('<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">','')
# impact,tth = meat.split('<br /><br /><hr /><small>')
# impact,tth = meat.split('</pre>')
post_data = {}
date = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
# print "m:"+meat
p = re.compile('(src="[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+)', re.I)
# p = re.compile("(http://[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+)", re.I)
url_list = p.findall(meat)
dir_paths = []
# dir_paths.append(u"images")
for url in url_list:
	flag = True
	tmp = url.replace(u'src="','')
	dirs = tmp.split(u'/')[0]
	for d in dir_paths:
		if d==dirs:
			flag = False
			break
	if flag:
		dir_paths.append(dirs)
	# print tmp
for dd in dir_paths:
	print dd
	meat = meat.replace('src="'+str(dd),'src="images')
print meat
post_data['title'] = title
post_data['soups'] = meat
en_post_data = urllib.urlencode(post_data)
try:
	# r1 = urllib2.urlopen('http://localhost:8000/isreport/upload',en_post_data)
	r1 = urllib2.urlopen('http://is.doshisha.ac.jp/isreport/upload',en_post_data)
	read = r1.read()
	print read
	if read ==u"1":
		commands.getoutput('echo "parse error:'+index+' '+date+'" >> script_result_author2.txt')
	elif read ==u"2":
		commands.getoutput('echo "already use number:'+index+' '+date+'" >> script_result_author2.txt')
	else:
		print "3"
		commands.getoutput('echo "OK:'+index+' to '+read+' '+date+'" >> script_result_author2.txt')
		commands.getoutput('mkdir '+read+'/images')
		cc = ""
		for dd in dir_paths:
			print dd
			cc += commands.getoutput('cp -r '+pp+'/'+dd+'/* '+read+'/images/')
		print "pp"+pp+" cc:"+cc
except:
	commands.getoutput('echo "INTERNAL SERVER ERROR:'+index+' '+date+'" >> script_result_author2.txt')