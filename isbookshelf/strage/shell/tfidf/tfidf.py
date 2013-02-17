#!/usr/bin/env python
# encoding: utf-8
#
# 名詞の出現頻度を数える
__usage__="""
count.py [raw text file] > [output file]
"""

import sys
sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/")
import MeCab
import os,re
import operator

t = MeCab.Tagger(" ".join(sys.argv))
ignones = []
words = {}
def to_int(value, default=None):
	try:
		i = int(value)
		return True
	except:
		return False
def parse(sentence):
	_data = t.parse(sentence)
	lines = _data.split(os.linesep)
	for row in lines:
		try:
			word_hinshi = row.split(",")[0]
			word,hinshi = word_hinshi.split("\t")
			if hinshi == '名詞':
				if len(word)<4:
					continue
				if to_int(word):
					continue
				if word in ignones:
					continue
				if not words.has_key(word):
					words[word] = 0
				words[word] += 1
		except:
			pass
#end def parse
if __name__ == '__main__':
	p1 = re.compile(u'<.*?>')
	p2 = re.compile(u'{=.*?=}')
	p3 = re.compile(u'{{.*?}}')
	f = "abst.txt"
	if len(sys.argv)>1:
		f = sys.argv[1]
	try:
		fd = file(f, "r")
	except:
		print __usage__
		sys.exit(0)
	for x in fd:
		# print x
		x = p1.sub('', x)
		x = p2.sub('', x)
		x = p3.sub('', x)
		parse(x)
	fd.close()
	items = words.items()
	items.sort(key=operator.itemgetter(1), reverse=True)
	for w,c in items:
		print "%d:%s\t%d" % (len(w),w,c)
	sys.exit(0)