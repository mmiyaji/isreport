#!/usr/bin/env python
# encoding: utf-8
"""
general.py

Created by Masahiro MIYAJI on 2011-05-08.
Copyright (c) 2011 ISDL. All rights reserved.
"""
import sys
from views import *

def MainPage(request):
	user = None
	appuser = None
	regist = False
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
	temp_values = Context()
	entry_count = Entry.get_count(regist)
	page=1
	temp_values['navi']=get_navi()
	# ranking = Entry.get_ranking(10)
	temp_values['ranking']=Entry.get_ranking(10)
	# temp_values['new_items']=new_item(0,5,regist)
	temp_values['new_items']=new_item(page=page,span=10,regist=regist)
	page_list,pages = get_page_list(page, entry_count, 10)
	temp_values['page_list']=page_list
	temp_values['pages']=pages
	temp_values['entry_count']=entry_count
	temp_values['target']="home"
	temp_values['target_url']="entry"
	temp_values['appuser']=appuser
	return render_to_response('isbookshelf/general/index.html',temp_values,
					context_instance=RequestContext(request))

# URL構造変更により今はほぼ使うことがない、以前の検索インデックスで飛んでくる人のために残している。リダイレクトさせてもいいかも
def CategoryPage(request):
	user = None
	appuser = None
	regist = False
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
	if request.method == 'GET':
		target = ""
		tar = ""
		temp_values = Context()
		if request.GET.has_key('target'):
			target = request.GET['target']
			tar += target

		if target == "group":
			template = 'isbookshelf/general/group.html'
			tar += "_/isreport/category?target="+target
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/category?target="+target+"&amp;page="+str(page)
			items,entry_count=Group.get_groups(page,GROUP_SPAN)
			temp_values['items']=items
			temp_values['entry_count']=entry_count
			page_list,pages = get_page_list(page, entry_count, GROUP_SPAN)
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['base_title']=u"研究グループ一覧"
			
		elif target == "author":
			template = 'isbookshelf/general/author_roll.html'
			auth_array = []
			# profs=Author.objects.order_by('-update_at').filter(rank="prof")
			# temp_values['profs']=profs
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="prof"),"rank":"教員 / Professor"})
			# temp_values['etcs']=etcs
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="etc"),"rank":"研究員 / Etcetera"})
			temp_values['items'] = auth_array
			# docs=Author.objects.order_by('-update_at').filter(rank="doc")
			# temp_values['docs']=docs
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="doc"),"rank":"博士課程後期 / Doctor"})
			# m2s=Author.objects.order_by('-update_at').filter(rank="m2")
			# temp_values['m2s']=m2s
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="m2"),"rank":"修士2年 / Master 2"})
			# m1s=Author.objects.order_by('-update_at').filter(rank="m1")
			# temp_values['m1s']=m1s
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="m1"),"rank":"修士1年 / Master 1"})
			# gras=Author.objects.order_by('-update_at').filter(rank="gra")
			# temp_values['gras']=gras
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="gra"),"rank":"学部4年 / Undergraduate 4"})
			# etcs=Author.objects.order_by('-update_at').filter(rank="etc")
			tar += "_/isreport/category?target="+target
			temp_years = []
			now_year = int(datetime.datetime.now().strftime("%Y"))
			for ye in xrange(openning_year, now_year+1):
				temp_years.append(str(ye))
			temp_values['years']=temp_years
			temp_values['base_title']=u"著者一覧"
		elif target == "year":
			template = 'isbookshelf/general/year.html'
			tar += "_/isreport/category?target="+target
			year = ""
			if request.GET.has_key('year'):
				year = request.GET['year']
				tar += ","+year+u"年_/isreport/category?target="+target+"&amp;year="+year
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/category?target="+target+"&amp;page="+str(page)
			items,entry_count=Entry.get_item(page=page,year=year)
			temp_values['items']=items
			temp_values['entry_count']=entry_count
			page_list,pages = get_page_list(page, entry_count, 10)
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['base_title']=u"年度別エントリー"+year
			temp_values['year']=year
			
		elif target == "renew":
			template = 'isbookshelf/general/renew.html'
			tar += "_/isreport/category?target="+target
			temp_values['base_title']=u"更新履歴一覧"
		elif target == "tag":
			template = 'isbookshelf/general/tag.html'
			tar += "_/isreport/category?target="+target
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/category?target="+target+"&amp;page="+str(page)
			items,entry_count=Tag.get_tags(page=page,span=TAG_SPAN)
			# tags=Tag.objects.order_by('-update_at')#[:10]
			temp_values['items']=items
			# temp_values['new_items']=new_item(page)
			temp_values['entry_count']=entry_count
			page_list,pages = get_page_list(page, entry_count, TAG_SPAN)
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['base_title']=u"タグ一覧"
			
		elif target == "new":
			template = 'isbookshelf/general/new.html'
			tar += "_/isreport/category?target="+target
			entry_count = Entry.get_count(regist)
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/category?target=new&amp;page="+str(page)
			temp_values['new_items']=new_item(page=page,span=NEW_SPAN,regist=regist)
			page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['base_title']=u"最新ISレポート一覧"
		elif target == "list":
			template = 'isbookshelf/general/author_list.html'
			years = []
			# temp_years = []
			now_year = int(datetime.datetime.now().strftime("%Y"))
			for ye in xrange(1, now_year+1-openning_year):
				ye_tmp = now_year+1-openning_year - ye
				years.append({"authors":Author.get_auth_year(int(ye_tmp)),"rank":str(ye_tmp)+"期生"})
			temp_values['items']=years
			temp_values['base_title']=u"著者一覧"
			tar += "_/isreport/category?target="+target
		elif target == "search":
			template = 'isbookshelf/general/searching.html'
			years = []
			# temp_years = []
			now_year = int(datetime.datetime.now().strftime("%Y"))
			for ye in xrange(1, now_year+1-openning_year):
				years.append(Author.get_auth_year(int(ye)))
			
			temp_values['years']=years
			temp_values['base_title']=u"詳細検索"
			tar += "_/isreport/category?target="+target
		else:
			template = 'isbookshelf/search.html'
			temp_values['base_title']=u"カテゴリー一覧"
			
		temp_values['appuser']=appuser
		temp_values['target']=target
		#print "tar:"+tar
		temp_values['navi']=get_navi(tar)
		return render_to_response(template,temp_values,
					context_instance=RequestContext(request))

# URL構造変更により今はほぼ使うことがない、以前の検索インデックスで飛んでくる人のために残している。リダイレクトさせてもいいかも
# contentsページ
def ContentsPage(request):
	user = None
	appuser = None
	regist = False
	approval = True
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if request.method == 'GET':
		target = ""
		target_id = ""
		author = ""
		year = ""
		tag = ""
		group = ""
		sauthor = ""
		stitle = ""
		sabst = ""
		search_description=""
		content = ""
		contents_target = ""
		tar = "Contents_/isreport/contents"
		temp_values = Context()
		template = 'isbookshelf/general/contents.html'
		para = ""
		if request.GET.has_key('target'):
			target = request.GET['target']
			tar += ","+target+"_/isreport/contents?target="+target
		if request.GET.has_key('targetid'):
			target_id = request.GET['targetid']
			tar += ","+target_id+"_/isreport/contents?targetid="+target_id
		if request.GET.has_key('author'):
			author = request.GET['author']
			tar += ",Author_/isreport/author?active=true,"+author+"_/isreport/author/"+author
			content = "author"
			contents_target = author
			target_author = Author.get_by_name(author)
			temp_values['para']="author="+target_author.name
			temp_values['target_url']="contents"
			temp_values['author']=target_author
			temp_values['base_title']=author+u"/"+target_author.roman+u" レポート一覧"
			template = 'isbookshelf/general/author_content.html'
			
		if request.GET.has_key('year'):
			year = request.GET['year']
			tar += ",Year_/isreport/year,"+year+"_/isreport/year/"+year
			content = "year"
			contents_target = year
			temp_values['base_title']=year+u"年度 レポート一覧"

		if request.GET.has_key('tag'):
			tag = request.GET['tag']
			tar += ",Tag_/isreport/category?target=tag,"+tag+"_/isreport/tag/"+tag
			content = "tag"
			contents_target = tag
			target_tag = Tag.get_by_name(tag)
			if not target_tag:
				# return HttpResponseRedirect("/isreport/notfound")
				raise Http404
			temp_values['base_title']=tag+u"のタグがついたレポート一覧"
			temp_values['para']="tag="+target_tag.name
			temp_values['target_url']="contents"
			temp_values['tag']=target_tag
			template = 'isbookshelf/general/tag_content.html'
			
		if request.GET.has_key('group'):
			group = request.GET['group']
			tar += ",Group_/isreport/group/,"+group+"_/isreport/group/"+group
			content = "group"
			contents_target = group
			target_group = Group.get_by_name(group)
			temp_values['group']=target_group
			temp_values['base_title']=group+u"グループ レポート一覧"
			temp_values['para']="group="+target_group.name
			temp_values['target_url']="contents"
			template = 'isbookshelf/general/group_content.html'
			
		# entry_count = Entry.get_count()
		if request.GET.has_key('entry'):
			entry = request.GET['entry']
			target_id = int(entry)
			entries = Entry.get_by_id(target_id)
			if entries:
				tar += ","+entries.title+"_/isreport/entry/"+entry
				content = "entry"
				contents_target = entry
				temp_values['base_title']=entries.title
				# temp_values['preview']=True
				if not entries.approval and not user:
					# return HttpResponseRedirect("/isreport/notfound")
					raise Http404
				template = 'isbookshelf/general/entry_def.html'
				# if True:
				try:
					org_htmls = open(JAM_DIR + entries.path +r"/indexorg.html").read()
					# org_htmls = open("/Users/mmiyaji/Subversion/isreport/isbooks/isbookshelf/templates/isbookshelf/component/report_sample.html").read()
					for i in entries.sorted_tags():
						# org_htmls += i.name.encode('utf-8').strip()
						org_htmls = org_htmls.replace(str(i.name.encode('utf-8').strip()),'<a class="keywd" href="/isreport/tag/'+ i.name.encode('utf-8') + '">' + i.name.encode('utf-8') + '</a>')
					temp_values['content_html'] = org_htmls
				except:
					temp_values['content_html'] = ""
			else:
				return HttpResponseRedirect("/isreport/notfound")
			# temp_values['author']=Author.get_by_name(author)

		if request.GET.has_key('stitle'):
			template = 'isbookshelf/general/searching.html'
			stitle = request.GET['stitle']
			# tar += u",Search_/isreport/category?target=search,Title検索【"+stitle+u"】_/isreport/contents?stitle="+stitle
			content = "stitle"
			contents_target = stitle
			temp_values['base_title']=u"Title検索【"+stitle+u"】"
			temp_values['target_url']=u"contents"
			if stitle:
				temp_values['stitle']=stitle
				search_description += u" Title検索【"+stitle+u"】"
				para += "&amp;stitle="+stitle
			
		if request.GET.has_key('sauthor'):
			template = 'isbookshelf/general/searching.html'
			sauthor = request.GET['sauthor']
			# tar += u",Search_/isreport/category?target=search,Author検索【"+sauthor+u"】_/isreport/contents?sauthor="+sauthor
			content = "sauthor"
			contents_target = sauthor
			temp_values['base_title']=u"Author検索【"+sauthor+u"】"
			temp_values['target_url']=u"contents"
			if sauthor:
				temp_values['sauthor']=sauthor
				search_description += u" Author検索【"+sauthor+u"】"
				para += "&amp;sauthor="+sauthor
		if request.GET.has_key('sabst'):
			template = 'isbookshelf/general/searching.html'
			sabst = request.GET['sabst']
			# tar += u",Search_/isreport/category?target=search,Abstract検索【"+sabst+u"】_/isreport/contents?sabst="+sabst
			content = "sabst"
			contents_target = sabst
			temp_values['base_title']=u"Abstract検索【"+sabst+u"】"
			temp_values['target_url']=u"contents"
			if sabst:
				temp_values['sabst']=sabst
				search_description += u" Abstract検索【"+sabst+u"】"
				para += "&amp;sabst="+sabst
		page=1
		if search_description:
			temp_values['search_description']=search_description
			temp_values['para']=para
			tar += u",Search_/isreport/category?target=search,"+search_description+"_/isreport/category?target=search"
		if request.GET.has_key('page'):
			page = int(request.GET['page'])
			tar += ",page"+str(page)+"_/isreport/contents?target="+target+"&page="+str(page)
		contents,entry_count = Entry.get_item(target=target,
									target_id=target_id,
									author=Author.get_by_name(author),
									year=year,
									tag=Tag.get_by_name(tag),
									group=Group.get_by_name(group),
									page=page,
									regist=regist,
									stitle=stitle,
									sauthor=sauthor,
									sabst=sabst,
									span=NEW_SPAN,
									approval=approval
								)
		
		page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
		temp_values['page_list']=page_list
		temp_values['pages']=pages
		temp_values['contents']=content
		temp_values['contents_target']=contents_target
		temp_values['appuser']=appuser
		temp_values['target']=target
		temp_values['navi']=get_navi(tar)
		# temp_values['new_items']=new_item()
		temp_values['contents_items']=contents
		
		return render_to_response(template,temp_values,
					context_instance=RequestContext(request))
	else:
		if user.is_staff:
			target = ""
			target_id = ""
			author = ""
			year = ""
			tag = ""
			group = ""

			sauthor = ""
			stitle = ""
			sabst = ""

			content = ""
			contents_target = ""
			search_description=""
			page=0
			para = ""
			tar = ""
			if request.POST.has_key('stag'):
				stag = request.POST['stag']
			if request.POST.has_key('stitle'):
				stitle = request.POST['stitle']
				search_description += u" Title検索【"+stitle+u"】"
				para += "&amp;stitle="+stitle
			if request.POST.has_key('sauthor'):
				sauthor = request.POST['sauthor']
				search_description += u" Author検索【"+sauthor+u"】"
				para += "&amp;sauthor="+sauthor
			if request.POST.has_key('sabst'):
				sabst = request.POST['sabst']
				search_description += u" Abstract検索【"+sabst+u"】"
				para += "&amp;sabst="+sabst
			contents,entry_count = Entry.get_item(target=target,
										target_id=target_id,
										author=Author.get_by_name(author),
										year=year,
										tag=Tag.get_by_name(tag),
										group=Group.get_by_name(group),
										page=page,
										regist=regist,
										stitle=stitle,
										sauthor=sauthor,
										sabst=sabst,
										span=1000
									)
			for entry in contents:
				# print entry.title
				# entry.tag.clear()
				if stag:
					t = Tag.get_by_name(stag)
					if t:
						entry.tag.add(t)
						t.save()
					else:
						t = Tag()
						t.name = stag
						t.create_by = appuser
						t.save()
						entry.tag.add(t)
			contents,entry_count = Entry.get_item(target=target,
										target_id=target_id,
										author=Author.get_by_name(author),
										year=year,
										tag=Tag.get_by_name(tag),
										group=Group.get_by_name(group),
										page=page,
										regist=regist,
										stitle=stitle,
										sauthor=sauthor,
										sabst=sabst,
										span=NEW_SPAN
									)
			temp_values = Context()
			page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
			tar += u",Search_/isreport/category?target=search,"+search_description+"_/isreport/category?target=search"
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/contents?target="+target+"&page="+str(page)
			temp_values['search_description']=search_description
			temp_values['para']=para
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['target']="search"
			temp_values['navi']=get_navi(tar)
			temp_values['base_title']=u"検索ページ"
			temp_values['contents_items']=contents
			temp_values['added']=True
			return render_to_response('isbookshelf/general/searching.html',temp_values,
							context_instance=RequestContext(request))
			return HttpResponseRedirect("/isreport/")
		else:
			# return HttpResponseRedirect("/isreport/forbidden")
			raise Http403

# entryページ
def EntryPage(request,ids=""):
	user = None
	appuser = None
	regist = False
	approval = True
	trans = True
	redirect = False
	org_htmls = ""
	htmls = ""
	description = ""
	tar = "Entry_/isreport/entry/"
	template = 'isbookshelf/general/entry.html'
	temp_values = Context()
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if ids:
		try:
			target_id = int(ids)
		except:
			raise Http404
		entry = Entry.get_by_id(target_id)
		if entry:
			description += entry.title
			if entry.abstract:
				description += u" - abstract「"+entry.abstract+u"」"
			tar += ","+entry.title+"_/isreport/entry/"+ids
			content = "entry"
			if not entry.approval and not user:
				# return HttpResponseRedirect("/isreport/forbidden")
				raise Http403
			if True:
				if entry.content:
					htmls = entry.content
					trans = False
				try:
					org_htmls = open(JAM_DIR + entry.path +r"/indexorg.html").read()
				except:
					org_htmls = u"no file"
				# org_htmls = open("/Users/mmiyaji/Subversion/isreport/isbooks/isbookshelf/templates/isbookshelf/component/report_sample.html").read()
				# for i in entry.sorted_tags():
				# 	# org_htmls += i.name.encode('utf-8').strip()
				# 	org_htmls = org_htmls.replace(str(i.name.encode('utf-8').strip()),'<a class="keywd" href="/isreport/tag/'+ i.name.encode('utf-8') + '">' + i.name.encode('utf-8') + '</a>')
			# except:
			# 	pass
				# org_htmls = open("/Users/mmiyaji/Subversion/isreport/isbooks/isbookshelf/templates/isbookshelf/component/report_sample.html").read()
				# for i in entry.sorted_tags():
				# 	# org_htmls += i.name.encode('utf-8').strip()
				# 	org_htmls = org_htmls.replace(str(i.name.encode('utf-8').strip()),'<a class="keywd" href="/isreport/tag/'+ i.name.encode('utf-8') + '">' + i.name.encode('utf-8') + '</a>')
		else:
			# return HttpResponseRedirect("/isreport/notfound")
			raise Http404
		
		if request.method == 'GET':
			# if appuser:
			echoes(appuser,DOMAIN+"/entry/"+ids,entry.title.replace('\"','\\"'),entry,request)
			if entry.upload_by.nickname == u"api":
				redirect = True
				trans = False
				# 	temp_values['description'] = description
				# 	temp_values['content_html'] = org_htmls
				# 	temp_values['target']="Entry"
				# 	temp_values['item']=entry
				# 	temp_values['navi']=get_navi(tar)
				# 	temp_values['htmls']=htmls
				# 	temp_values['trans']=trans
				# 	temp_values['math']=True
				# 	temp_values['base_title']=entry.title
				# 	return render_to_response(template,temp_values,
				# 		context_instance=RequestContext(request))
				# else:
				# 	return HttpResponseRedirect("/report/"+entry.path+"/index.html")
			# else:
			if True:
				temp_values['description'] = description
				temp_values['content_html'] = org_htmls
				temp_values['target']="Entry"
				temp_values['item']=entry
				# recom = calc_recom()
				# temp_values['recom_items']=recom
				temp_values['navi']=get_navi(tar)
				temp_values['ranking']=Entry.get_ranking(10)
				temp_values['htmls']=htmls
				temp_values['trans']=trans
				temp_values['redirect']=redirect
				temp_values['math']=True
				temp_values['base_title']=entry.title
				return render_to_response(template,temp_values,
					context_instance=RequestContext(request))
	else:
		description += "ISレポートの一覧ページです．"
		temp_values['description'] = description
		template = 'isbookshelf/general/new.html'
		target = "new"
		entry_count = Entry.get_count(regist)
		page=1
		if request.GET.has_key('page'):
			page = int(request.GET['page'])
			tar += ",page"+str(page)+"_/isreport/entry/&amp;page="+str(page)
		temp_values['new_items']=new_item(page=page,span=NEW_SPAN,regist=regist)
		page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
		temp_values['page_list']=page_list
		temp_values['pages']=pages
		temp_values['base_title']=u"最新ISレポート一覧"
		
		temp_values['target']=target
		temp_values['entry_count']=entry_count
		temp_values['target_url']="entry"
		temp_values['navi']=get_navi(tar)
		temp_values['ranking']=Entry.get_ranking(10)
		return render_to_response(template,temp_values,
			context_instance=RequestContext(request))
		
# authorページ
def AuthorPage(request,ids=""):
	user = None
	appuser = None
	regist = False
	approval = True
	org_htmls = ""
	target = ""
	description = ""
	tar = "Author_/isreport/author/"
	template = 'isbookshelf/general/author_content.html'
	temp_values = Context()
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if ids:
		author = Author.get_by_name(ids)
		# entry = Entry.get_by_id(target_id)
		if author:
			description += u"「"+author.name +u"」の作成したISレポート一覧ページです．"
			tar += ","+author.name+"_/isreport/author/"+author.name
			# temp_values['para']="author="+author.name
			temp_values['author']=author
			template = 'isbookshelf/general/author_content.html'
		else:
			raise Http404
			# return HttpResponseRedirect("/isreport/notfound")
		if request.method == 'GET':
			target="author"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/author/"+author.name+"?page="+str(page)
			contents,entry_count = Entry.get_item(
										author=author,
										page=page,
										regist=regist,
										span=NEW_SPAN,
										approval=approval
									)
			page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
			temp_values['description'] = description
			temp_values['page_list']=page_list
			temp_values['target_url']=target+"/"+author.name
			temp_values['pages']=pages
			temp_values['base_title']=author.name+u"/"+author.roman+u" レポート一覧"
			temp_values['appuser']=appuser
			temp_values['target']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			temp_values['author']=author
			# temp_values['new_items']=new_item()
			temp_values['contents_items']=contents
			return render_to_response(template,temp_values,
					context_instance=RequestContext(request))
	else:
		if request.GET.has_key('active'):
			description +=u"ISグループに現在在籍しているメンバー一覧ページです．"
			target = "author"
			template = 'isbookshelf/general/author_roll.html'
			auth_array = []
			# profs=Author.objects.order_by('-update_at').filter(rank="prof")
			# temp_values['profs']=profs
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="prof"),"rank":"教員 / Professor"})
			# temp_values['etcs']=etcs
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="etc"),"rank":"研究員 / Etcetera"})
			temp_values['items'] = auth_array
			# docs=Author.objects.order_by('-update_at').filter(rank="doc")
			# temp_values['docs']=docs
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="doc"),"rank":"博士課程後期 / Doctor"})
			# m2s=Author.objects.order_by('-update_at').filter(rank="m2")
			# temp_values['m2s']=m2s
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="m2"),"rank":"修士2年 / Master 2"})
			# m1s=Author.objects.order_by('-update_at').filter(rank="m1")
			# temp_values['m1s']=m1s
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="m1"),"rank":"修士1年 / Master 1"})
			# gras=Author.objects.order_by('-update_at').filter(rank="gra")
			# temp_values['gras']=gras
			auth_array.append({"authors":Author.objects.order_by('-update_at').filter(rank="gra"),"rank":"学部4年 / Undergraduate 4"})
			# etcs=Author.objects.order_by('-update_at').filter(rank="etc")
			tar += u",所属別_/isreport/author/?active=true"
			temp_years = []
			now_year = int(datetime.datetime.now().strftime("%Y"))
			for ye in xrange(openning_year, now_year+1):
				temp_years.append(str(ye))
			temp_values['years']=temp_years
			temp_values['description'] = description
			temp_values['base_title']=u"著者一覧"
			temp_values['target']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			return render_to_response(template,temp_values,
				context_instance=RequestContext(request))
		else:
			description +=u"ISグループのメンバー一覧ページです．"
			target = "list"
			template = 'isbookshelf/general/author_list.html'
			years = []
			# temp_years = []
			now_year = int(datetime.datetime.now().strftime("%Y"))
			for ye in xrange(1, now_year+1-openning_year):
				ye_tmp = now_year+1-openning_year - ye
				years.append({"authors":Author.get_auth_year(int(ye_tmp)),"rank":str(ye_tmp)+"期生"})
			temp_values['items']=years
			temp_values['description'] = description
			temp_values['base_title']=u"著者一覧"
			# tar += "_/isreport/author/"
			temp_values['target']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			return render_to_response(template,temp_values,
				context_instance=RequestContext(request))

# groupページ
def GroupPage(request,ids=""):
	user = None
	appuser = None
	regist = False
	approval = True
	org_htmls = ""
	target = ""
	description = ""
	tar = "Group_/isreport/group/"
	template = 'isbookshelf/general/group.html'
	temp_values = Context()
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if ids:
		group = Group.get_by_name(ids)
		# entry = Entry.get_by_id(target_id)
		if group:
			tar += ","+group.name+"_/isreport/group/"+group.name
			# temp_values['para']="author="+author.name
			description += u"「"+group.name+u"」研究グループのISレポート一覧ページです．"
			temp_values['group']=group
			template = 'isbookshelf/general/group_content.html'
		else:
			# return HttpResponseRedirect("/isreport/notfound")
			raise Http404
		if request.method == 'GET':
			target="group"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/group/"+group.name+"?page="+str(page)
			contents,entry_count = Entry.get_item(
										group=group,
										page=page,
										regist=regist,
										span=NEW_SPAN,
										approval=approval
									)
			page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
			temp_values['description'] = description
			temp_values['page_list']=page_list
			temp_values['target_url']=target+"/"+group.name
			temp_values['pages']=pages
			temp_values['base_title']=group.name+u" レポート一覧"
			temp_values['appuser']=appuser
			temp_values['target']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			temp_values['group']=group
			# temp_values['new_items']=new_item()
			temp_values['contents_items']=contents
			return render_to_response(template,temp_values,
					context_instance=RequestContext(request))
	else:
		if request.GET.has_key('active'):
			pass
		else:
			target = "group"
			description += u"ISグループの研究グループ一覧ページです．"
			template = 'isbookshelf/general/group.html'
			temp_values['target']=target
			tar += "_/isreport/group/"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/group/&amp;page="+str(page)
			items,entry_count=Group.get_groups(page,GROUP_SPAN)
			temp_values['description'] = description
			temp_values['items']=items
			temp_values['entry_count']=entry_count
			page_list,pages = get_page_list(page, entry_count, GROUP_SPAN)
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['target_url']=target
			temp_values['base_title']=u"研究グループ一覧"
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			return render_to_response(template,temp_values,
				context_instance=RequestContext(request))

# tagページ
def TagPage(request,ids=""):
	user = None
	appuser = None
	regist = False
	approval = True
	org_htmls = ""
	target = ""
	description = ""
	tar = "Tag_/isreport/tag/"
	template = 'isbookshelf/general/tag.html'
	temp_values = Context()
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if ids:
		tag = Tag.get_by_name(ids)
		# entry = Entry.get_by_id(target_id)
		if tag:
			description += u"「"+tag.name+u"」のタグがつけられたISレポート一覧ページです．"
			tar += ","+tag.name+"_/isreport/tag/"+tag.name
			temp_values['tag']=tag
			template = 'isbookshelf/general/tag_content.html'
		else:
			# return HttpResponseRedirect("/isreport/notfound")
			raise Http404
		if request.method == 'GET':
			target="tag"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/tag/"+tag.name+"?page="+str(page)
			contents,entry_count = Entry.get_item(
										tag=tag,
										page=page,
										regist=regist,
										span=NEW_SPAN,
										approval=approval
									)
			page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
			temp_values['description'] = description
			temp_values['page_list']=page_list
			temp_values['target_url']=target+"/"+tag.name
			temp_values['pages']=pages
			temp_values['base_title']=tag.name+u" レポート一覧"
			temp_values['appuser']=appuser
			temp_values['target']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			temp_values['tag']=tag
			# temp_values['new_items']=new_item()
			temp_values['contents_items']=contents
			return render_to_response(template,temp_values,
					context_instance=RequestContext(request))
	else:
		if request.GET.has_key('active'):
			pass
		else:
			target = "tag"
			description += "ISレポートにつけられているタグ(キーワード)の一覧ページです．"
			template = 'isbookshelf/general/tag.html'
			temp_values['target']=target
			tar += "_/isreport/tag/"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/tag/&amp;page="+str(page)
			items,entry_count=Tag.get_tags(page=page,span=TAG_SPAN)
			page_list,pages = get_page_list(page, entry_count, TAG_SPAN)
			temp_values['description'] = description
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['base_title']=u"タグ一覧"
			temp_values['items']=items
			temp_values['entry_count']=entry_count
			temp_values['target_url']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			return render_to_response(template,temp_values,
				context_instance=RequestContext(request))

# keywordページ
def KeywordPage(request,ids=""):
	user = None
	appuser = None
	regist = False
	approval = True
	org_htmls = ""
	target = ""
	description = ""
	view_level = 5
	tar = "Keyword_/isreport/keyword/"
	template = 'isbookshelf/general/keyword.html'
	temp_values = Context()
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if ids:
		tag = Word.get_by_name(ids)
		# entry = Entry.get_by_id(target_id)
		if tag:
			description += u"「"+tag.name+u"」のタグがつけられたISレポート一覧ページです．"
			tar += ","+tag.name+"_/isreport/keyword/"+tag.name
			temp_values['tag']=tag
			# template = 'isbookshelf/general/keyword_content.html'
			template = 'isbookshelf/general/keyword_network.html'
		else:
			# return HttpResponseRedirect("/isreport/notfound")
			raise Http404
		if request.method == 'GET':
			target="keyword"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/keyword/"+tag.name+"?page="+str(page)
			contents,entry_count = Entry.get_item(
										keyword=tag,
										page=page,
										regist=regist,
										span=NEW_SPAN,
										approval=approval
									)
			page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
			temp_values['description'] = description
			temp_values['page_list']=page_list
			temp_values['target_url']=target+"/"+tag.name
			temp_values['pages']=pages
			temp_values['base_title']=tag.name+u" レポート一覧"
			temp_values['appuser']=appuser
			temp_values['target']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			temp_values['tag']=tag
			# temp_values['new_items']=new_item()
			temp_values['contents_items']=contents
			return render_to_response(template,temp_values,
					context_instance=RequestContext(request))
	else:
		if request.GET.has_key('active'):
			pass
		else:
			target = "keyword"
			description += "ISレポートにつけられているタグ(キーワード)の一覧ページです．"
			template = 'isbookshelf/general/keyword.html'
			temp_values['target']=target
			tar += "_/isreport/keyword/"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/keyword/&amp;page="+str(page)
			# items,entry_count=Tag.get_tags(page=page,span=TAG_SPAN)
			items,entry_count=Word.get_words(page=page,span=KEYWORD_SPAN,view_level=view_level)
			page_list,pages = get_page_list(page, entry_count, KEYWORD_SPAN)
			temp_values['description'] = description
			temp_values['page_list']=page_list
			temp_values['pages']=pages
			temp_values['base_title']=u"キーワード一覧"
			temp_values['items']=items
			temp_values['entry_count']=entry_count
			temp_values['target_url']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			return render_to_response(template,temp_values,
				context_instance=RequestContext(request))

# yearページ
def YearPage(request,ids=""):
	user = None
	appuser = None
	regist = False
	approval = True
	org_htmls = ""
	target = ""
	description = ""
	tar = ""
	template = 'isbookshelf/general/year.html'
	temp_values = Context()
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if ids:
		year = ids
		tar += year+"_/isreport/year/"+year
		content = "year"
		description += u"「"+year+u"年度」に作成されたISレポート一覧ページです．"
		contents_target = year

		if request.method == 'GET':
			target="year"
			page=1
			if request.GET.has_key('page'):
				page = int(request.GET['page'])
				tar += ",page"+str(page)+"_/isreport/year/"+year+"?page="+str(page)
			items,entry_count = Entry.get_item(
										year=year,
										page=page,
										regist=regist,
										span=NEW_SPAN,
										approval=approval
									)
			page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
			temp_values['page_list']=page_list
			temp_values['target_url']=target+"/"+year
			temp_values['pages']=pages
			temp_values['base_title']=year+u"年度 レポート一覧"
			temp_values['appuser']=appuser
			temp_values['target']=target
			temp_values['navi']=get_navi(tar)
			temp_values['ranking']=Entry.get_ranking(10)
			temp_values['year']=year
			temp_values['items']=items
			# temp_values['new_items']=new_item()
			# temp_values['contents_items']=contents
			return render_to_response(template,temp_values,
					context_instance=RequestContext(request))

# Searchページ
def SearchPage(request,ids=""):
	user = None
	appuser = None
	regist = False
	approval = True
	year = ""
	sauthor = ""
	stitle = ""
	sabst = ""
	years = []
	sauthors = []
	stitles = []
	sabsts = []
	content = ""
	org_htmls = ""
	target = "search"
	tar = "Search_/isreport/search/"
	template = 'isbookshelf/general/searching.html'
	temp_values = Context()
	para =""
	description = u"ISレポート検索ページです．"
	search_description = ""
	temp_values['base_title']=""
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		regist = True
		approval = False
	if request.method == 'POST':
		if request.POST.has_key('stag'):
			stag = request.POST['stag']
		if request.POST.has_key('stitle'):
			stitle = request.POST['stitle']
			content = "stitle"
			contents_target = stitle
			if stitle:
				stitles = stitle.replace(u"　"," ").split(" ")
				temp_values['stitle']=stitle
				temp_values['base_title']+=u" Title検索【"+stitle+u"】"
				search_description += u" Title検索【"+stitle+u"】"
				para += "&amp;stitle="+stitle

		if request.POST.has_key('sauthor'):
			sauthor = request.POST['sauthor']
			content = "sauthor"
			contents_target = sauthor
			if sauthor:
				sauthors = sauthor.replace(u"　"," ").split(" ")
				temp_values['sauthor']=sauthor
				temp_values['base_title']+=u" Author検索【"+sauthor+u"】"
				search_description += u" Author検索【"+sauthor+u"】"
				para += "&amp;sauthor="+sauthor
		if request.POST.has_key('sabst'):
			sabst = request.POST['sabst']
			content = "sabst"
			contents_target = sabst
			if sabst:
				sabsts = sabst.replace(u"　"," ").split(" ")
				temp_values['sabst']=sabst
				temp_values['base_title']+=u" Abstract検索【"+sabst+u"】"
				search_description += u" Abstract検索【"+sabst+u"】"
				para += "&amp;sabst="+sabst
		page=1
		if search_description:
			temp_values['search_description']=search_description
			temp_values['para']=para
			temp_values['added']=True
			# tar += u","+search_description+"_/isreport/search/?"+para
			# if request.POST.has_key('page'):
			# 	page = int(request.POST['page'])
			# 	tar += ",page"+str(page)+"_/isreport/search/?"+para+"&amp;page="+str(page)
			contents,entry_count = Entry.get_item(
									page=page,
									regist=regist,
									# stitle=stitle,
									# sauthor=sauthor,
									# sabst=sabst,
									stitles=stitles,
									sauthors=sauthors,
									sabsts=sabsts,
									span=1000,
									approval=approval
								)
		# 検索結果に特定タグをつける
		for entry in contents:
			if stag:
				t = Tag.get_by_name(stag)
				if t:
					entry.tag.add(t)
					t.save()
				else:
					t = Tag()
					t.name = stag
					t.create_by = appuser
					t.save()
					entry.tag.add(t)
	else:
		if request.GET.has_key('stitle'):
			stitle = request.GET['stitle']
			content = "stitle"
			contents_target = stitle
			if stitle:
				stitles = stitle.replace(u"　"," ").split(" ")
				temp_values['stitle']=stitle
				temp_values['base_title']+=u" Title検索【"+stitle+u"】"
				search_description += u" Title検索【"+stitle+u"】"
				para += "&amp;stitle="+stitle
		
		if request.GET.has_key('sauthor'):
			sauthor = request.GET['sauthor']
			content = "sauthor"
			contents_target = sauthor
			if sauthor:
				sauthors = sauthor.replace(u"　"," ").split(" ")
				temp_values['sauthor']=sauthor
				temp_values['base_title']+=u" Author検索【"+sauthor+u"】"
				search_description += u" Author検索【"+sauthor+u"】"
				para += "&amp;sauthor="+sauthor
		if request.GET.has_key('sabst'):
			sabst = request.GET['sabst']
			content = "sabst"
			contents_target = sabst
			if sabst:
				sabsts = sabst.replace(u"　"," ").split(" ")
				temp_values['sabst']=sabst
				temp_values['base_title']+=u" Abstract検索【"+sabst+u"】"
				search_description += u" Abstract検索【"+sabst+u"】"
				para += "&amp;sabst="+sabst
		page=1
	if search_description:
		description += u"検索語句「"+search_description+u"」"
		temp_values['search_description']=search_description
		temp_values['para']=para
		tar += u","+search_description+"_/isreport/search/?"+para
		if request.GET.has_key('page'):
			page = int(request.GET['page'])
			tar += ",page"+str(page)+"_/isreport/search/?"+para+"&amp;page="+str(page)
		contents,entry_count = Entry.get_item(
								page=page,
								regist=regist,
								# stitle=stitle,
								# sauthor=sauthor,
								# sabst=sabst,
								stitles=stitles,
								sauthors=sauthors,
								sabsts=sabsts,
								span=NEW_SPAN,
								approval=approval
							)
		page_list,pages = get_page_list(page, entry_count, NEW_SPAN)
		temp_values['page_list']=page_list
		temp_values['pages']=pages
		temp_values['contents']=content
		temp_values['items']=contents
		# temp_values['contents_target']=contents_target
		years = []
		now_year = int(datetime.datetime.now().strftime("%Y"))
		for ye in xrange(1, now_year+1-openning_year):
			years.append(Author.get_auth_year(int(ye)))
		temp_values['years']=years
	temp_values['description'] = description
	temp_values['navi']=get_navi(tar)
	temp_values['ranking']=Entry.get_ranking(10)
	temp_values['target']=target
	temp_values['target_url']=u"search"
	temp_values['base_title']=u"詳細検索"
	return render_to_response(template,temp_values,
					context_instance=RequestContext(request))
	
	

		
# linkページ
def LinkPage(request):
	temp_values = Context()
	# temp_values['new_items']=new_item()
	temp_values['description'] = u"ISグループに関連のあるWebページの一覧ページです．"
	temp_values['target']="link"
	temp_values['navi']=get_navi("Link_/isreport/link")
	temp_values['ranking']=Entry.get_ranking(10)
	# temp_values['date']=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M")
	temp_values['base_title']=u"リンクページ"
	return render_to_response('isbookshelf/general/link.html',temp_values,
					context_instance=RequestContext(request))

# helpページ
def HelpPage(request):
	temp_values = Context()
	# temp_values['id']="";
	temp_values['description'] = u"ISレポートシステムの利用方法に関する事項が記載されたページです．"
	temp_values['target']="help"
	temp_values['navi']=get_navi("Help_/isreport/help/")
	temp_values['ranking']=Entry.get_ranking(10)
	temp_values['base_title']=u"ヘルプページ"
	# temp_values['date']=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M")
	return render_to_response('isbookshelf/general/help.html',temp_values,
					context_instance=RequestContext(request))

# helpページ
def ContactPage(request):
	temp_values = Context()
	# temp_values['id']="";
	temp_values['target']="contact"
	temp_values['navi']=get_navi("Contact_/isreport/contact/")
	temp_values['ranking']=Entry.get_ranking(10)
	temp_values['base_title']=u"連絡先"
	# temp_values['date']=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M")
	return render_to_response('isbookshelf/general/contact.html',temp_values,
					context_instance=RequestContext(request))

# renewページ
def RenewPage(request):
	temp_values = Context()
	template = 'isbookshelf/general/renew.html'
	temp_values['description'] = u"ISレポートシステムの更新履歴が記載されたページです．"
	temp_values['base_title']=u"更新履歴一覧"
	temp_values['target']="renew"
	temp_values['navi']=get_navi("Renew_/isreport/renew/")
	temp_values['ranking']=Entry.get_ranking(10)
	return render_to_response(template,temp_values,
					context_instance=RequestContext(request))

# 静的ページに移行．レポート許可時に再構築されます．
# rssページ
def RssPage(request):
	temp_values = Context()
	return render_to_response('isbookshelf/static/rss.xml',temp_values,
					mimetype = "text/xml; charset=utf-8",
					context_instance=RequestContext(request))
