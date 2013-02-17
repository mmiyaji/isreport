#!/usr/bin/env python
# encoding: utf-8
"""
ajax.py

Created by Masahiro MIYAJI on 2011-05-09.
Copyright (c) 2011 ISDL. All rights reserved.
"""
from views import *
from django.contrib.auth.decorators import login_required

def select_yearth(request):
	if request.GET.has_key('year'):
		target_year = request.GET['year']
		#print target_year
		authors = Author.get_auth_yearth(target_year)
		#print authors
		temp_values = Context()
		temp_values['authors']=authors
		return render_to_response('isbookshelf/component/author_list.html',temp_values,
						context_instance=RequestContext(request))

def select_author(request):
	authors = Author.auth_list()
	temp_values = Context()
	temp_values['authors']=authors
	return render_to_response('isbookshelf/component/author_list_ol.html',temp_values,
					context_instance=RequestContext(request))

def preview(request):
	temp_values = Context()
	entry = None
	if request.GET.has_key('id'):
		entry = Entry.get_by_id(int(request.GET['id']))
	temp_values['entry'] = entry
	temp_values['pub_year'] = entry.publish.strftime("%Y")
	return render_to_response('isbookshelf/component/preview.html',temp_values,
					context_instance=RequestContext(request))

def recommend(request,para):
	temp_values = Context()
	# entry = None
	if "id" in request.POST:
		ids = request.POST['id']
	else:
		if request.user.is_authenticated():
			ids = request.GET['id']
		else:
			raise Http404
	if para == "report":
		entry = Entry.get_by_id(int(ids))
	recom = calc_recom(request, new_entry=entry)
	temp_values['recom_items'] = recom
	# temp_values['pub_year'] = entry.publish.strftime("%Y")
	return render_to_response('isbookshelf/component/recommend.html',temp_values,
					context_instance=RequestContext(request))


@login_required
def ajax(request,para):
	if para =="img":
		temp_values = Context()
		entry = None
		if request.GET.has_key('id'):
			entry = Entry.get_by_id(int(request.GET['id']))
		temp_values['entry'] = entry
		return render_to_response('isbookshelf/component/inner_img.html',temp_values,
					context_instance=RequestContext(request))
	elif para =="nume":
		temp_values = Context()
		entry = None
		if request.GET.has_key('id'):
			entry = Entry.get_by_id(int(request.GET['id']))
		temp_values['entry'] = entry
		return render_to_response('isbookshelf/component/inner_numeric.html',temp_values,
					context_instance=RequestContext(request))
	elif para =="img_upload":
		temp_values = Context()
		entry = None
		if request.GET.has_key('id'):
			entry = Entry.get_by_id(int(request.GET['id']))
		temp_values['entry'] = entry
		return render_to_response('isbookshelf/component/inner_img_upload.html',temp_values,
					context_instance=RequestContext(request))
	elif para == "upload_img":
		return upload_img(request)
	elif para == "image_list":
		return image_list(request)
	elif para == "upload_numeric":
		return upload_numeric(request)
	elif para =="book":
		return get_books_form(request)

def get_books_form(request):
	user = None
	appuser = None
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
	if request.method == 'POST':
		target_book_id = request.POST['book_id']
		target_id = request.POST['target_id']
		target = Entry.get_by_id(int(target_id))
		if target_book_id == "-1":
			if request.POST.has_key('newbook'):
				new_book_title = request.POST['newbook']
				new_book = Book()
				new_book.title = new_book_title
				if request.POST.has_key('isvalid'):
					new_book.isvalid = True
				else:
					new_book.isvalid = False
				new_book.save()
				appuser.books.add(new_book)
				appuser.save()
				new_bh = BookHandler()
				new_bh.book = new_book
				new_bh.create_by = appuser
				new_bh.save()
				new_bh.entries.add(target)
				new_bh.save()
		elif target_book_id == "0":
			fh = FavoriteHandler.get_by_appuser(appuser)
			fh.entries.add(target)
			fh.save()
		else:
			target_book = Book.get_by_id(int(target_book_id))
			tbh = target_book.get_subs()
			tbh.entries.add(target)
			tbh.save()
		return HttpResponseRedirect("/isreport")
	else:
		if request.GET.has_key('id'):
			target_id = request.GET['id']
			target = Entry.get_by_id(int(target_id))
			temp_values = Context()
			temp_values['appuser']=appuser
			temp_values['target']=target
			return render_to_response('isbookshelf/component/books_form.html',temp_values,
						context_instance=RequestContext(request))
		else:
			raise Http404
			# return HttpResponseRedirect("/isreport/notfound")

def upload_img(request):
	msg = ''
	temp_values = Context()
	user = None
	appuser = None
	count = 1
	image_name = ""
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		# temp_values['appuser']=appuser
	entry = None
	entryid = ""
	dirpath = ""
	if True:
		if request.GET.has_key('id'):
			entryid = request.GET['id']
			if entryid:
				entry = Entry.get_by_id(int(entryid))
		if request.POST.has_key('id'):
			entryid = request.POST['id']
			if entryid:
				entry = Entry.get_by_id(int(entryid))
		dirpath = entry.path
		file_list = os.listdir(JAM_DIR + dirpath+r'/images/')
		# for files in file_list:
		# 	print files
		count = len(file_list)
		if request.method == 'POST':
			form = UploadFileForm(request.POST, request.FILES)
			image_name = entryid+"_image"
			# dirpath = request.POST['dirpath']
			# if request.POST.has_key('count'):
			# 	count = int(request.POST['count'])
			if request.POST.has_key('image_name'):
				image_name = request.POST['image_name']
			else:
				image_name += str(count)+".png"
				count +=1
			if request.FILES.has_key('file'):
				upfile = request.FILES['file']
				# print mimetypes.guess_type(upfile)
				updir = JAM_DIR + dirpath+r'/images/'+image_name #+ form.cleaned_data['title']
				#print "uppath"+updir
				destination = open(updir, 'wb+')
				for chunk in upfile.chunks():
					destination.write(chunk)
				destination.close()
				# print "get img"
				# content_type, width, height = getImageInfo(upfile)
				# print content_type
		file_list = os.listdir(JAM_DIR + dirpath+r'/images/')
	# except:
	# 	image_name = "http://m-server.appspot.com/download/picture-48_1.png?fid=aghtLXNlcnZlcnIQCxIIUG9zdERhdGEYrcMBDA"
	# 	file_list = ["http://m-server.appspot.com/download/picture-48_1.png?fid=aghtLXNlcnZlcnIQCxIIUG9zdERhdGEYrcMBDA"]
	# temp_values['file_list']= sorted(file_list)
	temp_values['file']=  image_name
	temp_values['image_url']= u'/report/'+dirpath+u'/images/'
	# temp_values['count']= count
	temp_values['entry']= entry
	return render_to_response('isbookshelf/component/inner_img_upload.html',temp_values,context_instance=RequestContext(request))

def image_list(request):
	msg = ''
	temp_values = Context()
	user = None
	appuser = None
	count = 1
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
	entry = None
	entryid = ""
	dirpath = ""
	if True:
		if request.GET.has_key('id'):
			entryid = request.GET['id']
			if entryid:
				entry = Entry.get_by_id(int(entryid))
		dirpath = entry.path
		file_list = os.listdir(JAM_DIR + dirpath+r'/images/')
	# except:
	# 	file_list = ["http://m-server.appspot.com","http://m-server.appspot.com","http://m-server.appspot.com","http://m-server.appspot.com"]
	# for files in file_list:
	# 	print files
	# file_list = os.listdir(JAM_DIR + dirpath+r'/images/')
	temp_values['file_list']= sorted(file_list)
	temp_values['image_url']= u'/report/'+dirpath+u'/images/'
	temp_values['entry']= entry
	return render_to_response('isbookshelf/component/image_list.html',temp_values,context_instance=RequestContext(request))

def upload_numeric(request):
	msg = ''
	temp_values = Context()
	user = None
	appuser = None
	count = 1
	image_name =""
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
	entry = None
	entryid = ""
	if request.GET.has_key('id'):
		entryid = request.GET['id']
		if entryid:
			entry = Entry.get_by_id(int(entryid))
	if request.POST.has_key('id'):
		entryid = request.POST['id']
		if entryid:
			entry = Entry.get_by_id(int(entryid))
	dirpath = entry.path
	file_list = os.listdir(JAM_DIR + dirpath+r'/images/')
	count = len(file_list)
	if request.method == 'POST':
		image_name = entryid+"_numeric"
		image_name += str(count)
		count +=1
		if request.POST.has_key('numeric'):
			numeric = request.POST['numeric']
			set_numeric(numeric,JAM_DIR + dirpath+r'/images/',image_name)
	file_list = os.listdir(JAM_DIR + dirpath+r'/images/')
	temp_values['file']= image_name
	temp_values['image_url']= u'/report/'+dirpath+u'/images/'
	temp_values['entry']= entry
	return render_to_response('isbookshelf/component/inner_numeric.html',temp_values,context_instance=RequestContext(request))

@login_required
def ajax_save(request):
	msg = ''
	isdraft = ""
	temp_values = Context()
	user = None
	appuser = None
	entry = None
	isstyle = False
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		temp_values['appuser']=appuser
	else:
		return HttpResponseForbidden()
	if request.POST.has_key('id'):
		entry = Entry.get_by_id(int(request.POST['id']))
		dirpath = entry.path
	else:
		# return HttpResponseRedirect("/isreport/notfound")
		raise Http404
	if request.method == 'POST':
		# print "POST"
		org = request.POST['soups']
		soups = request.POST['html_body']
		soups_def = request.POST['html_body_def']
		# print soups
		# print soups
		t_content = loader.get_template('isbookshelf/component/preview_html.html')
		c_content = Context()
		c_content['pub_year'] = entry.publish.strftime("%Y")
		c_content['title'] = entry.title
		c_content['html'] = soups_def
		soup_text = HttpResponse(t_content.render(c_content)).content
		# analyze = Analyze()
		# result = dict()
		try:
			# result = analyze.gets(soup_text)
			content_main = analyze.content_gets(soup_text)
			# 本文をデータベースに保存
			entry.content = content_main
		except:
			pass
		c_content['html'] = soups
		paths = JAM_DIR + dirpath
		form = UploadFileForm(request.POST, request.FILES)
		# if True:
		# try:
		# 	tmp_html = open(JAM_DIR + dirpath+"/index.html", "w")
		# 	tmp_html.write(soup_text)
		# 	tmp_html.close
		# except:
		# 	tmp_html = open(JAM_DIR + dirpath+"/index.html", "w")
		# 	tmp_html.write(org.encode('utf-8'))
		# 	tmp_html.close
		if True:
			tmp_html = open(JAM_DIR + dirpath+"/index.html", "w")
			tmp_html.write(HttpResponse(t_content.render(c_content)).content)
			tmp_html.close
		else:
			tmp_html = open(JAM_DIR + dirpath+"/index.html", "w")
			tmp_html.write(org.encode('utf-8'))
			tmp_html.close
		org_html = open(JAM_DIR + dirpath+"/indexorg.html", "wb+")
		org_html.write(org.encode('utf-8'))
		org_html.close
		entry.save()
		# return HttpResponse("OK")
	# temp_values = Context()
	temp_values['temp'] = "OK"
	return render_to_response('isbookshelf/component/temps.html',
				temp_values,context_instance=RequestContext(request))
@login_required
def change_favorite(request):
	user = None
	appuser = None
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		favorites = FavoriteHandler.get_by_appuser(appuser)
	if request.POST.has_key('id'):
		target_id = request.POST['id']
		target = Entry.get_by_id(int(target_id))
		if request.POST.has_key('reset'):
			favorites.entries.remove(target)
		else:
			favorites.entries.add(target)
		favorites.save()
		return HttpResponse("OK")
	else:
		return HttpResponse("NO")

@login_required
def remove_book(request):
	user = None
	appuser = None
	if request.user.is_authenticated():
		user = request.user
		appuser = ApplicationUser.get_by_user(user)
		if request.POST.has_key('bookid'):
			bookid = request.POST['bookid']
			if bookid=="0":
				bh = FavoriteHandler.get_by_appuser(appuser)
			else:
				book = Book.get_by_id(int(bookid))
				bh = BookHandler.get_by_book(book)
		if request.POST.has_key('id'):
			entryid = request.POST['id']
			entry = Entry.get_by_id(int(entryid))
			bh.entries.remove(entry)
			bh.save()
	return HttpResponseRedirect("/isreport/setting")

