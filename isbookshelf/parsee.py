#!/usr/bin/env python
# encoding: utf-8
"""
parse_html.py

Created by Masahiro MIYAJI on 2011-05-14.
Copyright (c) 2011 ISDL. All rights reserved.
"""

import os
import cookielib
import commands,simplejson
from cookielib import CookieJar, DefaultCookiePolicy
import urllib,urllib2,sys,re,time
# import string

# クッキーの設定
policy = cookielib.DefaultCookiePolicy(
		rfc2965=True, strict_ns_domain=DefaultCookiePolicy.DomainStrict,
		)
# クッキーオブジェクトの作成
cj = cookielib.CookieJar(policy)
# HTTPCookieProcessorにクッキーの処理を任せる。
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
url = "https://ajax.googleapis.com/ajax/services/language/translate"
class END(Exception):
    pass

class Parsee(object):
	def __init__(self):
		"""docstring for __init__"""
		self.splitter = ["?","!","．","：","；","？","！"]
		self.ignore = ["\*\*\*\*","\*\*\*","\*\*","\*","\-\-\-","\-\-","\-","\+\+\+","\+\+","\+","\#","\$\|","\>\?","\?\<","\$\%"]
		self.ignore_org = ["****","***","**","*","---","--","-","+++","++","+","#","$|",">?","?<","$%"]
		self.tag_ignore = ["<(/*)img(\"[^\"]*\"|'[^']*'|[^'\">])*>","<(/*)a(\"[^\"]*\"|'[^']*'|[^'\">])*>"]
		self.super_ignore = ["\%\%","\&\&"]
		self.super_ignore_org = ["%%","&&"]
		self.result = ""
		self.origin = ""
		self.html = ""

	def parse(self,html=""):
		"""docstring for parse"""
		if not html:
			html = self.html
		lines = html.splitlines()
		# print lines
		for line_count,i in enumerate(lines):
			# print line_count,"/",len(lines)
			if i:
				tmp = ""
				j,target,trans_flg,ign_flag = self.ignone(i)
				# print j,target,trans_flg,ign_flag
				if trans_flg:
					splits = self.splits(j)
					# print splits
					for j in splits:
						tran = self.trans(j)
						# print j
						# print tran
						self.origin += j
						tmp += tran
					if not ign_flag:
						tmp = target + tmp
					self.result += tmp
					self.result += "\n"
				else:
					# print i
					# print i
					self.result += i+"\n"
		return self.result
		
	def splits(self,text,ignore=""):
		array = []
		tmp = []
		find = False
		for c,i in enumerate(self.splitter):
			if ignore!=i:
				if text.count(i)>0:
					find = True
					tmp = text.split(i)
					for c2,j in enumerate(tmp):
						if c2==len(tmp)-1:
							array.extend(self.splits(j,ignore=i))
						else:
							array.extend(self.splits(j+i,ignore=i))
		if not find:
			array.append(text)
		return array
	
	def tag_ignone(self,text):
		tag_flag = True
		result = []
		target = ""
		try:
			for c,i in enumerate(self.tag_ignore):
				p = re.compile(i, re.I)
				ignore_list = p.findall(text)
				# print i,ignore_list
				# splitter = p.split(text)
				# print i,len(ignore_list),ignore_list
				# for ign in splitter:
				# 	print ign
				# 	result = ign
				# 	target = self.super_ignore_org[c]
				# 	raise END
		except END:
			tans_flag = False
			ign_flag = False
		return result
		
	def ignone(self,text):
		tans_flag = True
		ign_flag = True
		# tag_flag = True
		result = text
		target = ""
		
		try:
			for c,i in enumerate(self.ignore):
				p = re.compile("^"+i+"(.*)", re.I)
				ignore_list = p.findall(text)
				for ign in ignore_list:
					result = ign
					target = self.ignore_org[c]
					raise END
		except END:
			ign_flag = False
		try:
			for c,i in enumerate(self.super_ignore):
				p2 = re.compile("^"+i+"(.*)", re.I)
				ignore_list = p2.findall(text)
				for ign in ignore_list:
					result = ign
					target = self.super_ignore_org[c]
					raise END
		except END:
			tans_flag = False
			ign_flag = False
		return result,target,tans_flag,ign_flag

	def joint(self,htmls_array):
		for i in htmls_array:
			if i.count(">")>0:
				self.result += "<"
			arr = i.split(">")
			for c,j in enumerate(arr):
				self.result += j
				if not c==len(arr)-1:
					self.result += ">"
		# print self.result
	
	def trans(slef,text):
		if isinstance(text, unicode):
			text = text.encode('utf-8')
		post_data = {}
		post_data['v'] = "1.0"
		post_data['langpair'] = "ja|en"
		post_data['key'] = "AIzaSyBSjc5HyXyLvd2k5WIKsmWXoDojooVQnLA"
		post_data['q'] = text
		en_post_data = urllib.urlencode(post_data)
	
		req = urllib2.Request(url, en_post_data)
		# req.add_header('Content-Type', 'application/json')
		result = urllib2.urlopen(req).read()
		# print simplejson.loads(result).get('responseStatus')
		if simplejson.loads(result).get('responseStatus')==200:
			return simplejson.loads(result).get('responseData').get('translatedText')
		else:
			return text

	def trans1(self,text):
		# ?v=1.0&q=Hello,%20my%20frie<a>hoge</a>nd!&langpair=en%7Cja&key=AIzaSyBSjc5HyXyLvd2k5WIKsmWXoDojooVQnLA&resultFormat=text"
		
		r1 = urllib2.urlopen(url,en_post_data)
		return r1.read()
		# return read
def main():
	try:
		# 引数でパース先を決める
		# argvs = sys.argv
		# index = argvs[1]
		# commands.getoutput('echo "input:'+index+'" >> '+output)
		# index = "/Users/mmiyaji/Subversion/isreport/isbooks/isbookshelf/templates/isbookshelf/component/report_sample.html"
		index = "/Users/mmiyaji/Desktop/tmp/hoge2.html"
		htmls = open(index).read()
		parse = Parsee()
		parse.html = htmls
		# print htmls.translate(string.maketrans('aa', 'bc'))
		# print htmls
		# htmls_array = htmls.split("<")
	
		# t1 = time.time()
		# print parse.parse(htmls)
		# t2 =time.time()
		# print "time:",str(t2-t1)
		# print parse.tag_ignone(htmls)
	
		# f = "Schafferは，1985年に初めて多目的へGAを適用したアルゴリズム，ベクトル評価遺伝的アルゴリズム(Vector Evaluated Genetic Algorithm:VEGA)を提案した．VEGAという名は，各目的ベクトルを評価する手法であることに由来する．"
		# print f.count("?")
		
		# print parse.joint(htmls_array)
		# print parse.trans(htmls)
		
		# print parse.trans("非優越ソートを適用した場合の個体のランク付けの例を{{4}}に示す")
	except:
		pass

if __name__ == '__main__':
	main()

