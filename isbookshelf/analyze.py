# -*- coding: utf_8 -*-
import os, string, re, urllib, urllib2
from urllib2 import Request, urlopen, URLError, HTTPError

from BSXPath import BSXPathEvaluator,XPathResult
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString

class ValidationError(Exception):
	"""
	バリデーションエラー用の例外クラス
	"""

	def __init__(self, msg):
		Exception.__init__(self, msg)
		self.msg=msg

	def get_message(self):
		return self.msg


class BaseValidator(object):
	"""
	バリデータ用のベースクラス
	"""

	def validate(self, value):
		return value


class NotEmpty(BaseValidator):
	"""
	項目が空でないことを調べるバリデータ
	"""
	errors=("false")

	def validate(self, value):
		if not value:
#			raise ValidationError(self.errors[0]
			return ""
		return value


class IntValidator(BaseValidator):
	"""
	項目が整数の数値であることを調べるバリデータ
	"""
	errors=("no number")

	def validate(self, value):
		try:
			value=int(value)
		except ValueError:
#			raise ValidationError(self.errors[0])
			return ""
		if int(abs(value))!=abs(value):
#			raise ValidationError(self.errors[0])
			return ""
		return value

class NumValidator(BaseValidator):
	"""
	項目に数値があることを調べ、数字を抜き出すバリデータ
	"""
	errors=("no number")
	
	def validate(self, value):
		p = re.compile('[0-9]+')
		s = p.search(value)
		if s:
			return s.group()
		else:
#			raise ValidationError(self.errors[0])
			return ""

class SectionValidator(BaseValidator):
	"""
	Sectionから項目を抜き出すバリデータ
	"""
	errors=("NG")
	
	def validate(self, value):
		print "valids\n"+value
		value = re.compile("[\r|\n]+").split(value)
		# value = value.split(u"\n")
		if value:
			print "v:"+value
			return value
		else:
#			raise ValidationError(self.errors[0])
			return ""

class SpaceValidator(BaseValidator):
	"""
	&nbsp;をスペースに変換する
	"""
	errors=("NG")
	
	def validate(self, value):
		value = re.compile("&nbsp;").sub(" ",value)
		if value:
			return value
		else:
#			raise ValidationError(self.errors[0])
			return ""

class EliminateValidator(BaseValidator):
	"""
	\r,\nをスペースに変換する
	"""
	errors=("NG")
	
	def validate(self, value):
		value = re.compile("[\r|\n]+").sub(" ",value)
		if value:
			return value
		else:
#			raise ValidationError(self.errors[0])
			return ""


class IntRangeValidator(BaseValidator):
	"""
	値が一定の範囲にあることを調べるバリデータ
	"""
	errors=(u'入力された数値が設定された範囲を超えています。',)

	def __init__(self, min_val, max_val):
		self.min=min_val
		self.max=max_val

	def validate(self, value):
		value=IntValidator().validate(value)
		if value>self.max or self.min>value:
#			raise ValidationError(self.errors[0])
			return ""
		return value

class RegexValidator(BaseValidator):
	"""
	入力値が正規表現にマッチするかどうか調べるバリデータ
	"""
	errors=(u'正しい値を入力してください。',)
	return_value = True

	def __init__(self, pat):
		self.regex_pat=re.compile(pat)

	def validate(self, value):
		if not self.regex_pat.search(value):
#			raise ValidationError(self.errors[0])
			return ""
		else:
			if self.return_value:
				return self.return_value
			else:
				return value

class URLValidator(RegexValidator):
	"""
	URLとして正しい文字列かどうかを調べるバリデータ
	"""
	errors=('正しいURLを入力してください。')

	def __init__(self):
		self.regex_pat=re.compile('^(http|https)://[a-z0-9][a-z0-9\-\._]*\.[a-z]+(?:[0-9]+)?(?:/.*)?$', re.I)

class CssValidator(RegexValidator):
	"""
	CSSが正しいかどうかを調べるバリデータ
	"""
	errors=("false")

	def __init__(self):
		self.regex_pat=re.compile("http://mikilab.doshisha.ac.jp/dia/research/report/isdl_report.css")

class MikilabValidator(RegexValidator):
	"""
	CSSが正しいかどうかを調べるバリデータ
	"""
	errors=("false")

	def __init__(self):
		self.regex_pat=re.compile("mikilab.doshisha.ac.jp")

class AuthorHValidator(RegexValidator):
	"""
	Authorが正しいかどうかを調べるバリデータ
	"""
	errors=("false")

	def __init__(self):
		self.regex_pat=re.compile(u'廣安''[\s]?'u'知之')

class AuthorMValidator(RegexValidator):
	"""
	Authorが正しいかどうかを調べるバリデータ
	"""
	errors=("false")

	def __init__(self):
		self.regex_pat=re.compile(u'三木''[\s]?'u'光範')

class CopyrightHValidator(RegexValidator):
	"""
	copyrigthが正しいかどうかを調べるバリデータ
	"""
	errors=("false")

	def __init__(self):
		self.regex_pat=re.compile('Tomoyuki Hiroyasu')
		
class CopyrightMValidator(RegexValidator):
	"""
	copyrithが正しいかどうかを調べるバリデータ
	"""
	errors=("false")

	def __init__(self):
		self.regex_pat=re.compile('Mitsunori Miki')
		
class CopyrightYValidator(RegexValidator):
	"""
	copyrightの年が正しいかどうかを調べるバリデータ
	"""
	errors=("false")


class Analyze:
	# Initialize some global variables we will use
	def __init__(self):
		self._tmp = ""
		self.css_check = False
		self.author_h_check = False
		self.author_m_check = False
		self.number_check = False
		self.copyright_h_check = False
		self.copyright_m_check = False
		self.copyright_y_check = False
		self.error_point = [""]
		self.goes = True
		print "init"
	def empty(self):
		self._tmp = ""
		self._array = []
		
	def printText(self,tags):
		for tag in tags:
			if tag.__class__ == NavigableString:
				self._tmp += tag
			else:
				self.printText(tag)
		return self._tmp
	
	def printArray(self,tags):
		for tag in tags:
			if tag.__class__ == NavigableString:
				tag = SpaceValidator().validate(tag)
				self._array.append(tag)
			else:
				self.printArray(tag)
		return self._array
	
	def printContent(self,tags):
		print "printSec"
		for tag in tags:
			if tag:
				print tag.contents
				self._array.append(tag.contents)
			# if tag.__class__ == NavigableString:
			# 	tag = SpaceValidator().validate(tag)
			# 	self._array.append(tag)
			# else:
			# 	self.printArray(tag)
		return self._array
		
	def printList(self,tags):
		result = []
		
		for tag in tags:
			if tag.__class__ == NavigableString:
				self._tmp += tag
			else:
				result.append(SpaceValidator().validate(self._tmp))
				self.empty()
				self.printList(tag)
		return result	
	def content_gets(self, html):
		content = ""
		soup = BeautifulSoup(html)
		# soup = BeautifulSoup(soup.prettify())
		# if True:
		try:
			content = soup.find(id='content')
		except:
			pass
		return content
	def gets(self, html):
		# HTMLソースをBeautifulSoupに渡す
		soup = BeautifulSoup(html)
		# print soup.prettify()
		# soup = BeautifulSoup(soup.prettify())
		#css check
		css = soup.findAll("link",{'rel' : 'stylesheet'})
		for c in css:
			if c["href"]:
				self.css_check = CssValidator().validate(c["href"])
				if self.css_check:
					break
		
		#title check
		title = self.printText(soup.findAll("h1",{'id' : 'title'}))
		title = EliminateValidator().validate(title)
		print "title:"+title
		self.empty()
		
		#author check
		author = self.printText(soup.findAll("h3",{'id' : 'authors'}))
		self.author_h_check = AuthorHValidator().validate(author)
		self.author_m_check = AuthorMValidator().validate(author)
		print "author:"+author
		self.empty()
		
		#number check
		number = self.printText(soup.findAll("span",{'id' : 'report_num'}))
		# number = IntValidator().validate(NumValidator().validate(number))
		print "number:"+number
		
		# url_List = url.split("/")
		# if (url!="http://mikilab.doshisha.ac.jp/dia/research/report/report_sample/report20040407099.html"):
		# 	url_number = IntValidator().validate(NumValidator().validate(url_List[6] + url_List[7] + url_List[8]))
		# 	if (number == url_number):
		# 		self.number_check = True
		self.empty()
		
		#date check
		date = self.printText(soup.findAll("h4",{'id' : 'date'}))
		print "date:"+date
		
		self.empty()
		
		#abstract check
		abstract = self.printText(soup.findAll("span",{'id' : 'abstract_content'}))
		print "abstract:"+abstract
		self.empty()
		
		#section check
		section = self.printArray(soup.findAll("h3",{'class' : 'section'}))
		self.empty()
		section += self.printArray(soup.findAll("h4",{'class' : 'subsection'}))
		self.empty()
		section += self.printArray(soup.findAll("h5",{'class' : 'subsubsection'}))
		self.empty()
#		section = ""
#		for s in soup('h2',{'class' : 'section'}):
#			section += s.renderContents()
#		for s in soup('h3',{'class' : 'subsection'}):
#			section += s.renderContents()
#		for s in soup('h4',{'class' : 'subsubsection'}):
#			section += s.renderContents()
		# print "section:"
		# section = SpaceValidator().validate(section)
		# print "section:"+section
		# section = SectionValidator().validate(section)
		# for se in section:
		# 	print "section:"+se
		section.sort()
		while True:
			try:
				section.remove(u"")
			except:
				break
		for se in section:
			print "section:"+se
		section_List = section

		# section_content = (soup.findAll("div",{'class' : 'section_content'}))
		# self.empty()
		# subsection_content = (soup.findAll("div",{'class' : 'subsection_content'}))
		# self.empty()
		# subsubsection_content = (soup.findAll("div",{'class' : 'subsubsection_content'}))
		# self.empty()
		section_content = self.printContent(soup.findAll("div",{'class' : 'section_content'}))
		self.empty()
		subsection_content = self.printContent(soup.findAll("div",{'class' : 'subsection_content'}))
		self.empty()
		subsubsection_content = self.printContent(soup.findAll("div",{'class' : 'subsubsection_content'}))
		self.empty()
		print "sec"
		for se in section_content:
			print "*"+se
		print "subsec"
		for se in subsection_content:
			print "*"+se
		print "subsubsec"
		for se in subsubsection_content:
			print "*"+se
		# try:
		# 	section_List[-1] = section[-1].replace("References","")
		# 	section_List.append("References")
		# except:
		# 	pass
		
		# date = self.printText(soup.findAll("h4",{'class' : 'date'}))
		
		
		# print section[-1]
		# for s in section:
		# 	print s
			# section_List += s + u"¥n"
		
		#copyright check
		copyright = self.printText(soup.findAll("pre"))
		copyright = SpaceValidator().validate(copyright)
		self.copyright_h_check = CopyrightHValidator().validate(copyright)
		self.copyright_m_check = CopyrightMValidator().validate(copyright)
		# if (url!="http://mikilab.doshisha.ac.jp/dia/research/report/report_sample/report20040407099.html"):
		# 	self.copyright_y_check = RegexValidator(url_List[6]).validate(copyright)
		
		self.error_point.append(copyright.encode('utf_8'))
		print "copyright:"+copyright
		
		# print self.css_check
		# print self.author_h_check
		# print self.author_m_check
		# # print self.number_check
		# print self.copyright_h_check
		# print self.copyright_m_check
		# # print self.copyright_y_check
		# print title
		# print abstract
		# # print url
		# print section_List
		# print self.error_point
		# # print section.originalEncoding
		
		result = dict()
		result['css_check'] = self.css_check
		result['author_h_check'] = self.author_h_check
		result['author_m_check'] = self.author_m_check
		result['copyright_h_check'] = self.copyright_h_check
		result['copyright_m_check'] = self.copyright_m_check
		result['title'] = title
		
		date = date.replace(u"日","")
		date = date.replace(u"年",u"_")
		date = date.replace(u"月",u"_")
		date = date.replace(u" ","")
		
		dates = []
		dates = date.split(u"_")
		for i in dates:
			print i
		result['date'] = dates
		result['number'] = number

		# 余計な空白を削除。姓名の間の空白は削除しない
		# print author
		author = author.replace(u"，",u",")
		author = author.replace(u", ",u",")
		# print author
		author = author.replace(u" ,",u",")
		# print author
		author = author.rstrip()
		# print author
		author = author.lstrip()
		# print author
		result['author'] = author.split(",")
		result['abstract'] = abstract
		result['section_List'] = section_List
		result['error_point'] = self.error_point
		return result
		