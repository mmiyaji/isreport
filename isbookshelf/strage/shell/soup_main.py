#!/usr/bin/env python
# encoding: utf-8
"""
soup_main.py

Created by Masahiro MIYAJI on 2011-06-12.
Copyright (c) 2011 ISDL. All rights reserved.
"""

import sys
import os
from BeautifulSoup import BeautifulSoup,Comment
from BeautifulSoup import NavigableString

def main(index="/Users/mmiyaji/Desktop/tmp/hoge4.html"):
	args = sys.argv
	# index 
	if len(args)>1:
		index = args[1]
	html = open(index).read()
	soup = BeautifulSoup(html)
	soup = BeautifulSoup(soup.prettify())
	# soup = soup.findAll(text=lambda text:isinstance(text, Comment))
	result = ""
	ign = ["meta","script","style"]
	# print soup
	if True:
		content = soup.find(id='content')
		if content:
			result = str(content)
		else:
			content = soup.find(id='content_wrapper').contents[1]
			# next = content.next.nextSibling
			# while next:
			# 	print next.name
			# 	next = next.nextSibling
			flg = False
			for c,i in enumerate(content):
				# if not str(i).strip():
				# 	continue
				if i:
					if i.__class__ != NavigableString:
						try:
							name =  i.name
							print name,i.id
							if name in ign:
								continue
						except:
							pass
						try:
							classs = i['class']
							print i['class']
							if classs == "section":
								flg = True
							if classs == "header":
								flg = False
								continue
							# if classs == "header":
							# 	flg = True
							# 	continue
						except:
							pass
					try:
						if flg:
							# print i
							result += str(i)
					except:
						pass
		# content = soup.find(id='content_wrapper').contents[1]
		# links = soup.findAll('a')
		# for link in links:
		# 	print link.name                 # タグ名
		# 	print link.string               # タグの中のテキスト
		# 	print dict(link.attrs)['href']
	# except:
	# 	content = "error"
	# print content
	# print "###"
	# print result
	return result
if __name__ == '__main__':
	print main()

