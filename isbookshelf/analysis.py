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
		value = re.compile("[\r|\n]+").split(value)
		if value:
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


class Analyzer:
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
		
	def printText(self,tags):
		for tag in tags:
			if tag.__class__ == NavigableString:
				self._tmp += tag
			else:
				self.printText(tag)
		return self._tmp
		
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

		# for tag in tags:
		# 	# print tag
		# 	# print "$"
		# 	if tag.__class__ == NavigableString:
		# 		self._tmp += tag
		# 		# print tag
		# 		# print "???????"
		# 	else:
		# 		if tag.name != "p":
		# 			# result.append(SpaceValidator().validate(self._tmp)+"@")
		# 			result.append(res)
		# 			res =""
		# 		# print self._tmp
		# 		# print "#######"
		# 			# self.empty()
		# 			# self.printList(tag)
		# 		else:
		# 			try:
		# 				res += tag.string
		# 				res += "?"
		# 			except:
		# 				res += "#"
		# 				self.printList(tag)
					
		return result
	
	# def content_gets(self, html):
	# 	content = ""
	# 	soup = BeautifulSoup(html)
	# 	soup = BeautifulSoup(soup.prettify())
	# 	if True:
	# 		content = soup.find(id='content')
	# 	# except:
	# 	# 	pass
	# 	return content
	def gets(self, html):
			# 			# リクエストからメッセージ本文を取得
			# 			url = self.request.get("input_html")
			#
			# 			if not URLValidator().validate(url):
			# error = "Please input correct URL. "
			# path = os.path.join(os.path.dirname(__file__), 'index.html')
			# self.response.out.write(template.render(path, {"error":error,
			# 											 "url":url,
			# 											 }))
			# return
			# 
			# 			if not MikilabValidator().validate(url):
			# error = "It is not ISDL report URL. "
			# path = os.path.join(os.path.dirname(__file__), 'index.html')
			# self.response.out.write(template.render(path, {"error":error,
			# 											 "url":url,
			# 											 }))
			# return
			# 			
			# 			# クライアントを生成
			# 			opener = urllib2.build_opener()
			# 			try: opener.open(url).read()
			# 			except HTTPError, e:
			# error = e.code
			# path = os.path.join(os.path.dirname(__file__), 'index.html')
			# self.response.out.write(template.render(path, {"error":error,
			# 											 "url":url,
			# 											 }))
			# return
			# 			except URLError, e:
			# error = e.reason
			# path = os.path.join(os.path.dirname(__file__), 'index.html')
			# self.response.out.write(template.render(path, {"error":error,
			# 											 "url":url,
			# 											 }))
			# return
			# 			 
			# 			# クライアントを生成
			# 			opener = urllib2.build_opener() 
			# 			# HTMLソースを取得
			# 			html = opener.open(url).read()
		# HTMLソースをBeautifulSoupに渡す
		# print html
		# print "first"
		soup = BeautifulSoup(html)
		# print soup.prettify()
		# print soup
		print "soup"
		soup = BeautifulSoup(soup.prettify())
		#css check
		# css = soup.findAll("link",{'rel' : 'stylesheet'})
		# for c in css:
		# 	if c["href"]:
		# 		self.css_check = CssValidator().validate(c["href"])
		# 		if self.css_check:
		# 			break
		
		#title check
		title = self.printText(soup.findAll("h1",{'class' : 'title'}))
		title = EliminateValidator().validate(title)
		self.empty()
		# print title
		#author check
		author = self.printText(soup.findAll("h3",{'class' : 'author'}))
		# self.author_h_check = AuthorHValidator().validate(author)
		# self.author_m_check = AuthorMValidator().validate(author)
		self.empty()
		# print author
		#number check
		number = self.printText(soup.findAll("h4",{'class' : 'number'}))
		number = IntValidator().validate(NumValidator().validate(number))
		# url_List = url.split("/")
		# if (url!="http://mikilab.doshisha.ac.jp/dia/research/report/report_sample/report20040407099.html"):
		# 	url_number = IntValidator().validate(NumValidator().validate(url_List[6] + url_List[7] + url_List[8]))
		# 	if (number == url_number):
		# 		self.number_check = True
		# self.empty()
		# print number
		#date check
		date = self.printText(soup.findAll("h4",{'class' : 'date'}))
		self.empty()
		# print date
		#abstract check
		try:
			abstract = self.printText(soup.findAll("div",{'class' : 'abstract'}))
			self.empty()
			# print abstract
		except:
			abstract = ""
		#section check
# 		section_List = []
# 		try:
# 			section = self.printText(soup.findAll("h2",{'class' : 'section'}))
# 			self.empty()
# 			section += self.printText(soup.findAll("h3",{'class' : 'subsection'}))
# 			self.empty()
# 			section += self.printText(soup.findAll("h4",{'class' : 'subsubsection'}))
# 			self.empty()
# #		section = ""
# #		for s in soup('h2',{'class' : 'section'}):
# #			section += s.renderContents()
# #		for s in soup('h3',{'class' : 'subsection'}):
# #			section += s.renderContents()
# #		for s in soup('h4',{'class' : 'subsubsection'}):
# #			section += s.renderContents()
# 			
# 			section = SpaceValidator().validate(section)
# 			section = SectionValidator().validate(section)
# 			section.sort()
# 			while True:
# 				try:
# 					section.remove(u"")
# 				except:
# 					break
# 			section_List = section
# 			try:
# 				section_List[-1] = section[-1].replace("References","")
# 				section_List.append("References")
# 			except:
# 				pass
# 		except:
# 			pass
		date = self.printText(soup.findAll("h4",{'class' : 'date'}))
		
		# print section[-1]
		# for s in section:
		# 	print s
			# section_List += s + u"¥n"
		#copyright check
		# copyright = self.printText(soup.findAll("pre"))
		# copyright = SpaceValidator().validate(copyright)
		# self.copyright_h_check = CopyrightHValidator().validate(copyright)
		# self.copyright_m_check = CopyrightMValidator().validate(copyright)
		# if (url!="http://mikilab.doshisha.ac.jp/dia/research/report/report_sample/report20040407099.html"):
		# 	self.copyright_y_check = RegexValidator(url_List[6]).validate(copyright)
		
		# self.error_point.append(copyright.encode('utf_8'))
		
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
		# result['css_check'] = self.css_check
		# result['author_h_check'] = self.author_h_check
		# result['author_m_check'] = self.author_m_check
		# result['copyright_h_check'] = self.copyright_h_check
		# result['copyright_m_check'] = self.copyright_m_check
		result['title'] = title
		try:
			date = date.replace(u"日","")
			date = date.replace(u"年",u"_")
			date = date.replace(u"月",u"_")
			date = date.replace(u" ","")
			date = date.replace(u"\n","")
		except:
			date = u"2010_10_10"
		print "dada"
		print "DATE:"+date
		dates = []
		dates = date.split(u"_")
		for i in dates:
			print i
		result['date'] = dates
		result['number'] = number
		
		# print soup.encode('utf_8')
		# ssss = soup.replace(u"<p>",u"")#.replace(u"</p>","")
		# print "@@@@@@@"+ssss
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		result['body'] = soup
		print "checken1"


		# 余計な空白を削除。姓名の間の空白は削除しない
		# print author
		author = author.replace(u"　",u" ")
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
		# result['section_List'] = section_List
		result['error_point'] = self.error_point
		# result['taglist'] = self.printList(soup.findAll("p"))
		
		# print SpaceValidator().validate(html)
		
		# for p in soup.findAll(["p","h1","h2","h3"]):
		# 	print p.contents
		# 	print "@"
		print "###################################################################"
		return result
		
# 		path = os.path.join(os.path.dirname(__file__), 'index.html')
# 		self.response.out.write(template.render(path, {"css_check": self.css_check,
# 														 "author_h_check": self.author_h_check,
# 														 "author_m_check":self.author_m_check,
# 														 "number_check":self.number_check,
# 														 "copyright_h_check":self.copyright_h_check,
# 														 "copyright_m_check":self.copyright_m_check,
# 														 "copyright_y_check":self.copyright_y_check,
# 														 "title": title,
# 														 "abstract":abstract,
# 														 "url":url,
# 														 "section":section_List,
# 														 "error_point":self.error_point,
# #														 "enc":section.originalEncoding,
# 														 }))
# 		
# 	else:
# 	path = os.path.join(os.path.dirname(__file__), 'index.html')
# 	self.response.out.write(template.render(path, {"css_check": self.css_check,
# 													 "author_h_check": self.author_h_check,
# 													 "author_m_check":self.author_m_check,
# 													 "number_check":self.number_check,
# 													 "copyright_h_check":self.copyright_h_check,
# 													 "copyright_m_check":self.copyright_m_check,
# 													 "copyright_y_check":self.copyright_y_check,
# 													 }))

# # -*- coding: utf_8 -*-
# import os, string, re, urllib, urllib2
# from urllib2 import Request, urlopen, URLError, HTTPError
# 
# from BSXPath import BSXPathEvaluator,XPathResult
# from BeautifulSoup import BeautifulSoup
# from BeautifulSoup import NavigableString
# 
# class ValidationError(Exception):
# 	"""
# 	バリデーションエラー用の例外クラス
# 	"""
# 
# 	def __init__(self, msg):
# 		Exception.__init__(self, msg)
# 		self.msg=msg
# 
# 	def get_message(self):
# 		return self.msg
# 
# 
# class BaseValidator(object):
# 	"""
# 	バリデータ用のベースクラス
# 	"""
# 
# 	def validate(self, value):
# 		return value
# 
# 
# class NotEmpty(BaseValidator):
# 	"""
# 	項目が空でないことを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 	def validate(self, value):
# 		if not value:
# #			raise ValidationError(self.errors[0]
# 			return ""
# 		return value
# 
# 
# class IntValidator(BaseValidator):
# 	"""
# 	項目が整数の数値であることを調べるバリデータ
# 	"""
# 	errors=("no number")
# 
# 	def validate(self, value):
# 		try:
# 			value=int(value)
# 		except ValueError:
# #			raise ValidationError(self.errors[0])
# 			return ""
# 		if int(abs(value))!=abs(value):
# #			raise ValidationError(self.errors[0])
# 			return ""
# 		return value
# 
# class NumValidator(BaseValidator):
# 	"""
# 	項目に数値があることを調べ、数字を抜き出すバリデータ
# 	"""
# 	errors=("no number")
# 	
# 	def validate(self, value):
# 		p = re.compile('[0-9]+')
# 		s = p.search(value)
# 		if s:
# 			return s.group()
# 		else:
# #			raise ValidationError(self.errors[0])
# 			return ""
# 
# class SectionValidator(BaseValidator):
# 	"""
# 	Sectionから項目を抜き出すバリデータ
# 	"""
# 	errors=("NG")
# 	
# 	def validate(self, value):
# 		value = re.compile("[\r|\n]+").split(value)
# 		if value:
# 			return value
# 		else:
# #			raise ValidationError(self.errors[0])
# 			return ""
# 
# class SpaceValidator(BaseValidator):
# 	"""
# 	&nbsp;をスペースに変換する
# 	"""
# 	errors=("NG")
# 	
# 	def validate(self, value):
# 		value = re.compile("&nbsp;").sub(" ",value)
# 		if value:
# 			return value
# 		else:
# #			raise ValidationError(self.errors[0])
# 			return ""
# 
# class EliminateValidator(BaseValidator):
# 	"""
# 	\r,\nをスペースに変換する
# 	"""
# 	errors=("NG")
# 	
# 	def validate(self, value):
# 		value = re.compile("[\r|\n]+").sub(" ",value)
# 		if value:
# 			return value
# 		else:
# #			raise ValidationError(self.errors[0])
# 			return ""
# 
# 
# class IntRangeValidator(BaseValidator):
# 	"""
# 	値が一定の範囲にあることを調べるバリデータ
# 	"""
# 	errors=(u'入力された数値が設定された範囲を超えています。',)
# 
# 	def __init__(self, min_val, max_val):
# 		self.min=min_val
# 		self.max=max_val
# 
# 	def validate(self, value):
# 		value=IntValidator().validate(value)
# 		if value>self.max or self.min>value:
# #			raise ValidationError(self.errors[0])
# 			return ""
# 		return value
# 
# class RegexValidator(BaseValidator):
# 	"""
# 	入力値が正規表現にマッチするかどうか調べるバリデータ
# 	"""
# 	errors=(u'正しい値を入力してください。',)
# 	return_value = True
# 
# 	def __init__(self, pat):
# 		self.regex_pat=re.compile(pat)
# 
# 	def validate(self, value):
# 		if not self.regex_pat.search(value):
# #			raise ValidationError(self.errors[0])
# 			return ""
# 		else:
# 			if self.return_value:
# 				return self.return_value
# 			else:
# 				return value
# 
# class URLValidator(RegexValidator):
# 	"""
# 	URLとして正しい文字列かどうかを調べるバリデータ
# 	"""
# 	errors=('正しいURLを入力してください。')
# 
# 	def __init__(self):
# 		self.regex_pat=re.compile('^(http|https)://[a-z0-9][a-z0-9\-\._]*\.[a-z]+(?:[0-9]+)?(?:/.*)?$', re.I)
# 
# class CssValidator(RegexValidator):
# 	"""
# 	CSSが正しいかどうかを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 	def __init__(self):
# 		self.regex_pat=re.compile("http://mikilab.doshisha.ac.jp/dia/research/report/isdl_report.css")
# 
# class MikilabValidator(RegexValidator):
# 	"""
# 	CSSが正しいかどうかを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 	def __init__(self):
# 		self.regex_pat=re.compile("mikilab.doshisha.ac.jp")
# 
# class AuthorHValidator(RegexValidator):
# 	"""
# 	Authorが正しいかどうかを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 	def __init__(self):
# 		self.regex_pat=re.compile(u'廣安''[\s]?'u'知之')
# 
# class AuthorMValidator(RegexValidator):
# 	"""
# 	Authorが正しいかどうかを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 	def __init__(self):
# 		self.regex_pat=re.compile(u'三木''[\s]?'u'光範')
# 
# class CopyrightHValidator(RegexValidator):
# 	"""
# 	copyrigthが正しいかどうかを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 	def __init__(self):
# 		self.regex_pat=re.compile('Tomoyuki Hiroyasu')
# 		
# class CopyrightMValidator(RegexValidator):
# 	"""
# 	copyrithが正しいかどうかを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 	def __init__(self):
# 		self.regex_pat=re.compile('Mitsunori Miki')
# 		
# class CopyrightYValidator(RegexValidator):
# 	"""
# 	copyrightの年が正しいかどうかを調べるバリデータ
# 	"""
# 	errors=("false")
# 
# 
# class Analyzer:
# 	# Initialize some global variables we will use
# 	def __init__(self):
# 		self._tmp = ""
# 		self.css_check = False
# 		self.author_h_check = False
# 		self.author_m_check = False
# 		self.number_check = False
# 		self.copyright_h_check = False
# 		self.copyright_m_check = False
# 		self.copyright_y_check = False
# 		self.error_point = [""]
# 		self.goes = True
# 		print "init"
# 	def empty(self):
# 		self._tmp = ""
# 		
# 	def printText(self,tags):
# 		for tag in tags:
# 			if tag.__class__ == NavigableString:
# 				self._tmp += tag
# 			else:
# 				self.printText(tag)
# 		return self._tmp
# 		
# 	def printList(self,tags):
# 		result = []
# 		
# 		for tag in tags:
# 			if tag.__class__ == NavigableString:
# 				self._tmp += tag
# 			else:
# 				result.append(SpaceValidator().validate(self._tmp))
# 				self.empty()
# 				self.printList(tag)
# 		return result
# 
# 		# for tag in tags:
# 		# 	# print tag
# 		# 	# print "$"
# 		# 	if tag.__class__ == NavigableString:
# 		# 		self._tmp += tag
# 		# 		# print tag
# 		# 		# print "???????"
# 		# 	else:
# 		# 		if tag.name != "p":
# 		# 			# result.append(SpaceValidator().validate(self._tmp)+"@")
# 		# 			result.append(res)
# 		# 			res =""
# 		# 		# print self._tmp
# 		# 		# print "#######"
# 		# 			# self.empty()
# 		# 			# self.printList(tag)
# 		# 		else:
# 		# 			try:
# 		# 				res += tag.string
# 		# 				res += "?"
# 		# 			except:
# 		# 				res += "#"
# 		# 				self.printList(tag)
# 					
# 		return result
# 	
# 	
# 	def gets(self, html):
# 			# 			# リクエストからメッセージ本文を取得
# 			# 			url = self.request.get("input_html")
# 			#
# 			# 			if not URLValidator().validate(url):
# 			# error = "Please input correct URL. "
# 			# path = os.path.join(os.path.dirname(__file__), 'index.html')
# 			# self.response.out.write(template.render(path, {"error":error,
# 			# 											 "url":url,
# 			# 											 }))
# 			# return
# 			# 
# 			# 			if not MikilabValidator().validate(url):
# 			# error = "It is not ISDL report URL. "
# 			# path = os.path.join(os.path.dirname(__file__), 'index.html')
# 			# self.response.out.write(template.render(path, {"error":error,
# 			# 											 "url":url,
# 			# 											 }))
# 			# return
# 			# 			
# 			# 			# クライアントを生成
# 			# 			opener = urllib2.build_opener()
# 			# 			try: opener.open(url).read()
# 			# 			except HTTPError, e:
# 			# error = e.code
# 			# path = os.path.join(os.path.dirname(__file__), 'index.html')
# 			# self.response.out.write(template.render(path, {"error":error,
# 			# 											 "url":url,
# 			# 											 }))
# 			# return
# 			# 			except URLError, e:
# 			# error = e.reason
# 			# path = os.path.join(os.path.dirname(__file__), 'index.html')
# 			# self.response.out.write(template.render(path, {"error":error,
# 			# 											 "url":url,
# 			# 											 }))
# 			# return
# 			# 			 
# 			# 			# クライアントを生成
# 			# 			opener = urllib2.build_opener() 
# 			# 			# HTMLソースを取得
# 			# 			html = opener.open(url).read()
# 		# HTMLソースをBeautifulSoupに渡す
# 		# print html
# 		soup = BeautifulSoup(html)
# 		# print soup.prettify()
# 		# print soup
# 		soup = BeautifulSoup(soup.prettify())
# 		#css check
# 		css = soup.findAll("link",{'rel' : 'stylesheet'})
# 		for c in css:
# 			if c["href"]:
# 				self.css_check = CssValidator().validate(c["href"])
# 				if self.css_check:
# 					break
# 		
# 		#title check
# 		title = self.printText(soup.findAll("h1",{'class' : 'title'}))
# 		title = EliminateValidator().validate(title)
# 		self.empty()
# 		#author check
# 		author = self.printText(soup.findAll("h3",{'class' : 'author'}))
# 		self.author_h_check = AuthorHValidator().validate(author)
# 		self.author_m_check = AuthorMValidator().validate(author)
# 		self.empty()
# 		
# 		#number check
# 		number = self.printText(soup.findAll("h4",{'class' : 'number'}))
# 		number = IntValidator().validate(NumValidator().validate(number))
# 		# url_List = url.split("/")
# 		# if (url!="http://mikilab.doshisha.ac.jp/dia/research/report/report_sample/report20040407099.html"):
# 		# 	url_number = IntValidator().validate(NumValidator().validate(url_List[6] + url_List[7] + url_List[8]))
# 		# 	if (number == url_number):
# 		# 		self.number_check = True
# 		# self.empty()
# 		
# 		#date check
# 		date = self.printText(soup.findAll("h4",{'class' : 'date'}))
# 		self.empty()
# 		
# 		#abstract check
# 		abstract = self.printText(soup.findAll("div",{'class' : 'abstract'}))
# 		self.empty()
# 		
# 		#section check
# 		section_List = []
# 		try:
# 			section = self.printText(soup.findAll("h2",{'class' : 'section'}))
# 			self.empty()
# 			section += self.printText(soup.findAll("h3",{'class' : 'subsection'}))
# 			self.empty()
# 			section += self.printText(soup.findAll("h4",{'class' : 'subsubsection'}))
# 			self.empty()
# #		section = ""
# #		for s in soup('h2',{'class' : 'section'}):
# #			section += s.renderContents()
# #		for s in soup('h3',{'class' : 'subsection'}):
# #			section += s.renderContents()
# #		for s in soup('h4',{'class' : 'subsubsection'}):
# #			section += s.renderContents()
# 			
# 			section = SpaceValidator().validate(section)
# 			section = SectionValidator().validate(section)
# 			section.sort()
# 			while True:
# 				try:
# 					section.remove(u"")
# 				except:
# 					break
# 			section_List = section
# 			try:
# 				section_List[-1] = section[-1].replace("References","")
# 				section_List.append("References")
# 			except:
# 				pass
# 		except:
# 			pass
# 		date = self.printText(soup.findAll("h4",{'class' : 'date'}))
# 		
# 		# print section[-1]
# 		# for s in section:
# 		# 	print s
# 			# section_List += s + u"¥n"
# 		#copyright check
# 		copyright = self.printText(soup.findAll("pre"))
# 		copyright = SpaceValidator().validate(copyright)
# 		self.copyright_h_check = CopyrightHValidator().validate(copyright)
# 		self.copyright_m_check = CopyrightMValidator().validate(copyright)
# 		# if (url!="http://mikilab.doshisha.ac.jp/dia/research/report/report_sample/report20040407099.html"):
# 		# 	self.copyright_y_check = RegexValidator(url_List[6]).validate(copyright)
# 		
# 		self.error_point.append(copyright.encode('utf_8'))
# 		
# 		# print self.css_check
# 		# print self.author_h_check
# 		# print self.author_m_check
# 		# # print self.number_check
# 		# print self.copyright_h_check
# 		# print self.copyright_m_check
# 		# # print self.copyright_y_check
# 		# print title
# 		# print abstract
# 		# # print url
# 		# print section_List
# 		# print self.error_point
# 		# # print section.originalEncoding
# 		result = dict()
# 		result['css_check'] = self.css_check
# 		result['author_h_check'] = self.author_h_check
# 		result['author_m_check'] = self.author_m_check
# 		result['copyright_h_check'] = self.copyright_h_check
# 		result['copyright_m_check'] = self.copyright_m_check
# 		result['title'] = title
# 		
# 		date = date.replace(u"日","")
# 		date = date.replace(u"年",u"_")
# 		date = date.replace(u"月",u"_")
# 		date = date.replace(u" ","")
# 		date = date.replace(u"\n","")
# 		
# 		dates = []
# 		dates = date.split(u"_")
# 		for i in dates:
# 			print i
# 		result['date'] = dates
# 		result['number'] = number
# 		
# 		# print soup.encode('utf_8')
# 		# ssss = soup.replace(u"<p>",u"")#.replace(u"</p>","")
# 		# print "@@@@@@@"+ssss
# 		result['body'] = soup
# 		print "checken1"
# 
# 
# 		# 余計な空白を削除。姓名の間の空白は削除しない
# 		# print author
# 		author = author.replace(u"　",u" ")
# 		author = author.replace(u"，",u",")
# 		author = author.replace(u", ",u",")
# 		# print author
# 		author = author.replace(u" ,",u",")
# 		# print author
# 		author = author.rstrip()
# 		# print author
# 		author = author.lstrip()
# 		# print author
# 		result['author'] = author.split(",")
# 		result['abstract'] = abstract
# 		result['section_List'] = section_List
# 		result['error_point'] = self.error_point
# 		# result['taglist'] = self.printList(soup.findAll("p"))
# 		
# 		# print SpaceValidator().validate(html)
# 		
# 		# for p in soup.findAll(["p","h1","h2","h3"]):
# 		# 	print p.contents
# 		# 	print "@"
# 		return result
# 		
# # 		path = os.path.join(os.path.dirname(__file__), 'index.html')
# # 		self.response.out.write(template.render(path, {"css_check": self.css_check,
# # 														 "author_h_check": self.author_h_check,
# # 														 "author_m_check":self.author_m_check,
# # 														 "number_check":self.number_check,
# # 														 "copyright_h_check":self.copyright_h_check,
# # 														 "copyright_m_check":self.copyright_m_check,
# # 														 "copyright_y_check":self.copyright_y_check,
# # 														 "title": title,
# # 														 "abstract":abstract,
# # 														 "url":url,
# # 														 "section":section_List,
# # 														 "error_point":self.error_point,
# # #														 "enc":section.originalEncoding,
# # 														 }))
# # 		
# # 	else:
# # 	path = os.path.join(os.path.dirname(__file__), 'index.html')
# # 	self.response.out.write(template.render(path, {"css_check": self.css_check,
# # 													 "author_h_check": self.author_h_check,
# # 													 "author_m_check":self.author_m_check,
# # 													 "number_check":self.number_check,
# # 													 "copyright_h_check":self.copyright_h_check,
# # 													 "copyright_m_check":self.copyright_m_check,
# # 													 "copyright_y_check":self.copyright_y_check,
# # 													 }))
