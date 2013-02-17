#!/usr/bin/ python
# -*- coding: utf-8 -*-
import cookielib
import commands
from cookielib import CookieJar, DefaultCookiePolicy
import urllib,urllib2,sys
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
output = "script_result1004.txt"
try:
	# 引数でパース先を決める
	argvs = sys.argv
	index = argvs[1]
	commands.getoutput('echo "input:'+index+'" >> '+output)
	p = index.split("/")
	pp = ""
	for i in range(len(p)-1):
		print p[i]
		pp +=p[i]+"/"
		print pp
# path = index.replace("/index.html","")
# .lastIndexOf("1");
# allLines = open('/Users/mmiyaji/MJ/2010/program/django/isapps/isbooks/isbookshelf/templates/isbookshelf/isdl_sample.html').read()
	allLines = open(index).read()

# 4期小野対策：タグが大文字、クラス属性に""なし
	allLines = allLines.replace('<BODY>','<body>')
	allLines = allLines.replace('</BODY>','</body>')
	allLines = allLines.replace('<TITLE>','<title>')
	allLines = allLines.replace('</TITLE>','</title>')
	allLines = allLines.replace('<PRE>','<pre>')
	allLines = allLines.replace('</PRE>','</pre>')
	allLines = allLines.replace('<DIV','<div')
	allLines = allLines.replace('DIV>','div>')
	allLines = allLines.replace('<H1','<h1')
	allLines = allLines.replace('H1>','h1>')
	allLines = allLines.replace('<H2','<h2')
	allLines = allLines.replace('H2>','h2>')
	allLines = allLines.replace('<H3','<h3')
	allLines = allLines.replace('H3>','h3>')
	allLines = allLines.replace('<H4','<h4')
	allLines = allLines.replace('H4>','h4>')
	allLines = allLines.replace('<A','<a')
	allLines = allLines.replace('A>','a>')
	allLines = allLines.replace('</A','</a')
	allLines = allLines.replace('<P','<p')
	allLines = allLines.replace('P>','p>')
	allLines = allLines.replace('<HR','<hr')
	allLines = allLines.replace('HR>','hr>')
	allLines = allLines.replace('<CENTER','<center')
	allLines = allLines.replace('CENTER>','center>')

	allLines = allLines.replace('<div class=body>','<div class="body">')
	allLines = allLines.replace('<div class=header>','<div class="header">')
	allLines = allLines.replace('<h1 class=title>','<h1 class="title">')
	allLines = allLines.replace('<h3 class=author>','<h3 class="author">')
	allLines = allLines.replace('<h4 class=number>','<h4 class="number">')
	allLines = allLines.replace('<h4 class=date>','<h4 class="date">')
	allLines = allLines.replace('<h2 class=abstract>','<h2 class="abstract">')
	allLines = allLines.replace('<div class=abstract>','<div class="abstract">')
	allLines = allLines.replace('<h2 class=section>','<h2 class="section">')
	allLines = allLines.replace('</a href>','</a>')
	allLines = allLines.replace('<div class=caption>','<div class="caption">')
	allLines = allLines.replace('<h2 class=copyright>','<h2 class="copyright">')

# 9期生大西 祥代対策 ""開始抜け
	allLines = allLines.replace('<dl compact">','<dl>')

# 8期生朝山対策 <div class="body">がたくさんある
	allLines = allLines.replace('<div align="center"><a href="../../">Back to Top</a></div>','')

# 平岩 健一郎 name属性に“”なし
	allLines = allLines.replace('<a name=[1]>','<a name="[1]">')
	allLines = allLines.replace('<a name=[2]>','<a name="[2]">')

# 宮崎 真 =なし
	allLines = allLines.replace('<a href"','<a href="')
# 伊藤 冬子 name属性に“”なし
	allLines = allLines.replace('<a name=Bib::aqg>','<a name="Bib::aqg">')
# 吉井 健吾name属性に“”なし
	allLines = allLines.replace('<A name=tth_sEc5>','<A name="tth_sEc5">')

# 吉井 健吾 これはむり対応策ふめい
# <h1 class="title"> マスタースレーブモデルにおける並列・分散遺伝的アルゴリズムの検討
#   <!-- ------------------
#     著者名（自分の氏名と，教員の氏名を書く）
# -------------------- -->
# </h1>
# """	  <!-- ------------------
# 	    著者名（自分の氏名と，教員の氏名を書く）
# 	-------------------- -->"""

# 吉井 健吾
	allLines = allLines.replace('<h2 class=section>','<h2 class="section">')
# 千野晋平 ""なし多数 タグ大文字

# 今里 和弘
	allLines = allLines.replace('class=copyright','class="copyright"')
	allLines = allLines.replace('name=copyright','name="copyright"')

	allLines = allLines.replace('class=body','class="body"')
	allLines = allLines.replace('class=header','class="header"')
	allLines = allLines.replace('class=title','class="title"')
	allLines = allLines.replace('class=author','class="author"')
	allLines = allLines.replace('class=number','class="number"')
	allLines = allLines.replace('class=date','class="date"')
	allLines = allLines.replace('class=abstract','class="abstract"')
	allLines = allLines.replace('class=section','class="section"')
	allLines = allLines.replace('class=subsection','class="subsection"')

# 後藤 和宏，吉井 健吾
	try:
		allLines = allLines.replace('src=img/燃料電池の原理2.gif','src="img/燃料電池の原理2.gif"')
	except:
		pass
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
	print meat
	post_data = {}
	post_data['title'] = title
	post_data['soups'] = meat
	en_post_data = urllib.urlencode(post_data)
	date = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
except:
	commands.getoutput('echo "error:'+index+'" >> '+output)
try:
	# r1 = urllib2.urlopen('http://localhost:8000/isreport/upload',en_post_data)
	r1 = urllib2.urlopen('http://is.doshisha.ac.jp/isreport/upload',en_post_data)
	read = r1.read()
	print "read:"+read
	if read ==u"1":
		commands.getoutput('echo "parse error:'+index+' '+date+'" >> '+output)
	elif read ==u"2":
		commands.getoutput('echo "already use number:'+index+' '+date+'" >> '+output)
	else:
		print "3"
		commands.getoutput('echo "OK:'+index+' to '+read+' '+date+'" >> '+output)
		cc = commands.getoutput('cp -r '+pp+'/* '+read+'/')
		print "pp"+pp+" cc:"+cc
except:
	commands.getoutput('echo "INTERNAL SERVER ERROR:'+index+'" >> '+output)
	
