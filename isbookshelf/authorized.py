#!/usr/bin/env python
# encoding: utf-8
"""
general.py

Created by Masahiro MIYAJI on 2011-05-08.
Copyright (c) 2011 ISDL. All rights reserved.
"""
from views import *
from base64 import b64decode
from django.contrib.auth.decorators import login_required
# from analysis import Analyzer
from analyze import Analyze

@login_required
def basic_auth(request):
    # auth_header = request.headers.get('Authorization')
    isbase = True
    if True:
        if True:
            isbase = True
            base_user = APP_USER
            base_pass = create_hash(APP_PASSWD)
    if isbase:
        if True:
            try:
                # print "#####",request.META
                # (scheme, base64) = auth_header.split(' ')
                (scheme, base64) = request.META['HTTP_AUTHORIZATION'].split()
                if scheme != 'Basic':
                    return False
                (username, password) = b64decode(base64).split(':')
                if username == base_user and create_hash(password) == base_pass:
                    return True
            except (ValueError,TypeError,KeyError), err:
                logging.warn(type(err))
                return False
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="IS Report System"'
        # response.set_status(401)
        # response.headers['WWW-Authenticate'] = 'Basic realm="IS Report System"'
    else:
        return True

# user作成
def create_user(request):
    try:
        name = request.POST['username']
        password = request.POST['password']
        secret = create_hash(request.POST['secret'])
        if len(name) < 1 or len(password) < 1:
            error = "name or password is empty"
            return render_to_response('isbookshelf/authorized/login.html',
                                {'createError':error,'username':name,'pass':password},
                                context_instance=RequestContext(request))

        if User.objects.filter(username=name):
            error = "Sorry. Can't use this account"
            return render_to_response('isbookshelf/authorized/login.html',
                                {'createError':error,'username':name,'pass':password},
                                context_instance=RequestContext(request))
        if secret == APP_PASSWD or secret == ADMIN_PASS:
            user = User.objects.create_user(name, '', password)
            user.save()
            if secret == ADMIN_PASS:
                user.is_staff = True
                user.is_superuser = True
            user.save()
            appuser = ApplicationUser()
            appuser.user = user
            appuser.nickname = name
            appuser.save()
            # fav = Favorite()
            # fav.save()
            fh = FavoriteHandler()
            fh.create_by = appuser
            fh.save()
            makes = mkdir(USER_DIR+"/"+name)
            users = authenticate(username=name, password=password)
            if users is not None:
                if users.is_active:
                    login(request, users)
                    return HttpResponseRedirect('/isreport/setting?is_first=true')
                                    # Redirect to a success page.
             #   else:
                    # Return a 'disabled account' error mess
             #else:
                # Return an 'invalid login' error message.
                return HttpResponseRedirect('/isreport/setting?is_first=true')
            return HttpResponseRedirect('/isreport/setting?is_first=true')
        else:
            error = "新規アカウント作成時にはSecret IDの入力が必須です．"
            return render_to_response('isbookshelf/authorized/login.html',
                                {'createError':error,'username':name,'pass':password,'create':True},
                                context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect('/isreport')

# userログイン
def login_user(request):
    try:
        name = request.POST['username']
        password = request.POST['password']
        users = authenticate(username=name, password=password)
        if users is not None:
            if users.is_active:
                login(request, users)
                return HttpResponseRedirect('/isreport')
            else:
                return more_try(request,name,password)
        return more_try(request,name,password)
    except:
        return more_try(request,name,password)

def more_try(request,name,password):
    error = u"入力されたユーザ名･パスワードは正しくありません．"
    return render_to_response('isbookshelf/authorized/login.html',
                        {'loginError':error,'username':name,'pass':password},
                        context_instance=RequestContext(request))

# loginページ 間違っても関数loginをオーバーライドしないこと
def LoginPage(request):
    if request.method == 'POST':
        if request.POST.has_key('create'):
            return create_user(request)
        else:
            return login_user(request)
    else:
        # if basic_auth(request):
        if True:
            temp_values = Context()
            if request.GET.has_key('create'):
                temp_values['create']=True
            temp_values['navi']=get_navi("login_/isreport/login")
            # temp_values['new_items']=new_item()
            temp_values['target']="login"
            temp_values['base_title']=u"ログインページ"
            return render_to_response('isbookshelf/authorized/login.html',temp_values,
                        context_instance=RequestContext(request))

# logoutページ
def LogoutPage(request):
    auth.logout(request)
    return HttpResponseRedirect("/isreport")


# アーカイブ化
@login_required
def DownloadPage(request):
    if request.method == 'POST':
#        return HttpResponseRedirect("/isreport")
        return get_epub(request)
    else:
        temp_values = Context()
        user = None
        appuser = None
        if request.user.is_authenticated():
            user = request.user
            appuser = ApplicationUser.get_by_user(user)
            favorites = FavoriteHandler.get_by_appuser(appuser)
            temp_values['appuser']=appuser
            temp_values['fav_items']=favorites
            if request.GET.has_key('book'):
                bks = Book.get_by_id(request.GET['book'])
                if bks:
                    temp_values['selecter'] = bks
                    temp_values['fav_items'] = bks.get_subs()
                    temp_values['base_title']=bks.title+u" ダウンロードページ"
            temp_values['target']="download"
            temp_values['navi']=get_navi("download_/isreport/epub")

        return render_to_response('isbookshelf/authorized/epub_form.html',temp_values,
                        context_instance=RequestContext(request))

# epub形式にする前に 指定したディレクトリへ必要ファイルをまとめる
def get_epub(request):
    user = None
    appuser = None
    temp_values = Context()
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
    # else:
    #     return HttpResponseRedirect("/isreport/epub?error=unauthorized")
    title = request.POST['e_title']
    username = request.POST['e_author']
    items = request.POST.getlist('items')
    entries = []
    for item in items:
        entry = Entry.get_by_id(int(item))
        if entry:
            entries.append(entry)
    book = None
    book_id = "unknown"
    if request.POST.has_key('bookid'):
        bookid = request.POST['bookid']
        if bookid:
            book = Book.get_by_id(bookid)
            book_id = str(book.id)
        else:
            book_id = appuser.nickname#+u"'s favorite"
    if request.POST.has_key('anony'):
        appuser = book.get_owner()
    dirpath = appuser.nickname+"/isreport_"+book_id
    set_template(USER_DIR+"/"+dirpath)

    e_title = title
    e_creater = username
    e_bookid = book_id
    e_publisher = u"IS"
    e_list = []
    count = 1
    for entry in entries:
        coun = ""
        if count < 10:
            coun = u"0"+str(count)
        else:
            coun = str(count)
        item = Context()
        item['id'] = entry.id
        item['ref'] = u"chap"+coun+u".xhtml"
        item['title'] = entry.title
        item['entry'] = entry
        e_list.append(item)
        count +=1
    e_author = user
    e_own_page = "http://is.doshisha.ac.jp"
    e_own_name = "IS Group"
    ss=""
    t_content = loader.get_template('isbookshelf/oebps/content.opf')
    c_content = Context()
    c_content['title'] = e_title
    c_content['creater'] = e_creater
    c_content['bookid'] = e_bookid
    c_content['publisher'] = e_publisher
    c_content['list'] = e_list

    o_content = open(USER_DIR+"/"+dirpath+"/OEBPS/content.opf", "w")
    o_content.write(HttpResponse(t_content.render(c_content)).content)
    o_content.close

    t_title = loader.get_template('isbookshelf/oebps/title_page.xhtml')
    c_title = Context()
    c_title['title'] = e_title
    c_title['author'] = e_author
    c_title['publisher'] = e_publisher
    c_title['own_page'] = e_own_page
    c_title['own_name'] = e_own_name

    o_title = open(USER_DIR+"/"+dirpath+"/OEBPS/title_page.xhtml", "w")
    o_title.write(HttpResponse(t_title.render(c_title)).content)
    o_title.close

    t_agenda = loader.get_template('isbookshelf/oebps/agenda.xhtml')
    c_agenda = Context()
    c_agenda['list'] = e_list

    o_agenda = open(USER_DIR+"/"+dirpath+"/OEBPS/agenda.xhtml", "w")
    o_agenda.write(HttpResponse(t_agenda.render(c_agenda)).content)
    o_agenda.close

    t_toc = loader.get_template('isbookshelf/oebps/toc.ncx')
    c_toc = Context()
    c_toc['title'] = e_title
    c_toc['bookid'] = e_bookid
    c_toc['list'] = e_list

    o_toc = open(USER_DIR+"/"+dirpath+"/OEBPS/toc.ncx", "w")
    o_toc.write(HttpResponse(t_toc.render(c_toc)).content)
    o_toc.close
    # ver. full path
    dirpath = USER_DIR+"/"+dirpath
    count = 1
    for entry in entries:
        coun = ""
        if count < 10:
            coun = u"0"+str(count)
        else:
            coun = str(count)
        addr = u"chap"+coun+u".xhtml"
        mvtemplate(JAM_DIR+entry.path,dirpath+u"/OEBPS",addr)
        # if entry.isapi:
        #print "$$$$$$$"+addr
        if entry.upload_by.nickname == u"api":
            #print "#######"
            file_list = os.listdir(JAM_DIR+entry.path)
            for flist in file_list:
                #print "input:"+flist
                if flist == "images":
                    continue
                elif flist == "index.html":
                    continue
                elif flist == "index.html":
                    continue
                elif flist == "indexorg.html":
                    continue
                elif flist == "META-INF":
                    continue
                elif flist == "mimetype":
                    continue
                elif flist == "OEBPS":
                    continue
                elif flist == "css":
                    continue
                #print "REACH:"+flist
                mvstatics(JAM_DIR+entry.path,dirpath+u"/OEBPS",flist)
            # images
            # index.html
            # indexorg.html
            # META-INF
            # mimetype
            # OEBPS
        count +=1
    # ダウンロードページに飛ばす
    t_down = 'isbookshelf/authorized/epub_download.html'
    c_down = Context()
    c_down['path'] = dirpath
    c_down['book_title'] = e_title
    c_down['book_id'] = e_bookid
    c_down['entries'] = entries
    c_down['target']="download"
    temp_values['base_title']=e_title+u"　ダウンロードページ"
#    return HttpResponseRedirect("/isreport/epub")
    return render_to_response(t_down,c_down,context_instance=RequestContext(request))

# 指定したディレクトリをepub形式に圧縮する
def zipper(request):
    target = request.GET['id']
    entry = Entry.get_by_id(int(target))
    user = u"isreport"+str(entry.num)
    dirpath = JAM_DIR + entry.path
    if entry.upload_by.nickname == u"api":
        file_list = os.listdir(JAM_DIR+entry.path)
        for flist in file_list:
            # print "input:"+flist
            if flist == "images":
                continue
            elif flist == "index.html":
                continue
            elif flist == "index.html":
                continue
            elif flist == "indexorg.html":
                continue
            elif flist == "META-INF":
                continue
            elif flist == "mimetype":
                continue
            elif flist == "OEBPS":
                continue
            elif flist == "css":
                continue
            #print "REACH:"+flist
            mvstatics(JAM_DIR+entry.path,dirpath+u"/OEBPS",flist)

    zipub(dirpath,user)
    response = HttpResponse(open(dirpath+"/"+user+".epub",'rb').read(), mimetype='application/epub+zip')
    response['Content-Disposition'] = 'filename='+user+'.epub'
    return response

# 指定したディレクトリをepub形式に圧縮する
def zip(request):
    if request.method == 'POST':
        dirpath = request.POST['dirpath']
        bookid = request.POST['book_id']
        user = u"isreport_"+bookid
        zipub(dirpath,user)
        return zipped(request)
    else:
        return render_to_response('isbookshelf/authorized/epub_form.html',
                        context_instance=RequestContext(request))
# 圧縮関数
def zipped(request):
    # t_down = loader.get_template('isbookshelf/download.html')
    # t_down = 'isbookshelf/download.html'
    c_down = Context()
    dirpath = request.POST['dirpath']
    c_down['path'] = dirpath.replace("/var/www","")
    name = dirpath.split("/")[-1]
    # return HttpResponseRedirect(DOMAIN+c_down['path']+"/"+name+".epub")
    # response = HttpResponse(mimetype='application/epub+zip')
    # response['Content-Disposition'] = 'attachment; filename='+DOMAIN+c_down['path']+'/'+name+'.epub'
    # return response
    response = HttpResponse(open(DOCUMENT_DIR+c_down['path']+"/"+name+".epub",'rb').read(), mimetype='application/epub+zip')
    # response = HttpResponse(open(c_down['path']+"/"+name+".epub",'rb').read(), mimetype='application/epub+zip')
    response['Content-Disposition'] = 'filename='+name+'.epub'
    return response
    # return HttpResponse(t_down.render(c_down))
    # return render_to_response(t_down,c_down,context_instance=RequestContext(request))


# #######################
# 以下エディタ関係
# #######################

# form版upload
@login_required
def WritePage(request):
    msg = ''
    temp_values = Context()
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
        temp_values['appuser']=appuser
        temp_years = []
        now_year = int(datetime.datetime.now().strftime("%Y"))
        for ye in xrange(openning_year, now_year+1):
            temp_years.append(str(ye))
        temp_values['years']=temp_years
        temp_values['now_year']=str(now_year)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # html = request.POST['html_body']
        # temp_values['html'] = html
        number = request.POST['number']
        title = request.POST['title']
        authors = request.POST.getlist('authors')
        groups = []
        if request.POST.has_key('groups'):
            groups = request.POST.getlist('groups')
        date = request.POST['date']
        date = date.replace(u"　","").replace(u" ","").replace(u"日","").replace(u"年","-").replace(u"月","-")
        abstract = request.POST['abstract']
        # section = request.POST['section']
        dirpath = request.POST['dirpath']
        if number and authors and title:
            number = Entry.isfirst(number)
            if number:
                dirpath = ""
                if request.POST.has_key('private'):
                    dirpath = "private"
                    mkdir(JAM_DIR + dirpath)
                    dirpath += "/"
                # dirpath = JAM_DIR
                # dirpath = r'/Library/WebServer/Documents/isbooks/'
                dirpath += date.split("-")[0]
                mkdir(JAM_DIR + dirpath)
                dirpath += "/"
                dirpath += date.split("-")[1]
                mkdir(JAM_DIR + dirpath)
                dirpath += "/"
                dirpath += date.split("-")[2]
                mkdir(JAM_DIR + dirpath)
                dirpath += "/"
                dirpath += str(number)
                mkdir(JAM_DIR + dirpath)
                set_static(JAM_DIR + dirpath)
                # t_content = loader.get_template('isbookshelf/preview_html.html')
                # c_content = Context()
                # c_content['title'] = title
                # c_content['html'] = html
                # tmp_html = open(dirpath+"/index.html", "w")
                # tmp_html.write(HttpResponse(t_content.render(c_content)).content)
                # tmp_html.close
                # org_html = open(dirpath+"/indexorg.html", "wb+")
                # org_html.write(html.encode('utf-8'))
                # org_html.close
            else:
                return HttpResponseRedirect("/isreport/upload_form?error=1")
        else:
            return HttpResponseRedirect("/isreport/upload_form?error=alreadyuse")
        entry = Entry()
        entry.path = dirpath
        entry.title = title
        entry.abstract = abstract
        # entry.section = section
        entry.num = number

        published = datetime.datetime(int(date.split("-")[0]),int(date.split("-")[1]),int(date.split("-")[2]))
        entry.publish = published
        entry.upload_by = appuser
        if request.POST.has_key('private'):
            entry.ispublic = False
        entry.save()
        ii = ""
        for auth in authors:
            ii += str(auth)+u","
            au = Author.get_by_id(int(auth))
            if au:
                entry.author.add(au)
        entry.tmp1 = ii
        if request.POST.has_key('author_list'):
            author_list = request.POST['author_list']
        for gro in groups:
            gr = Group.get_by_id(int(gro))
            if gr:
                entry.group.add(gr)
                gr.save()
        if request.POST.has_key('tags'):
            tag_list = []
            tags = request.POST['tags']
            tag_list = tags.split(",")
            entry.tag.clear()
            for tag in tag_list:
                if tag:
                    t = Tag.get_by_name(tag)
                    if t:
                        entry.tag.add(t)
                        t.save()
                    else:
                        t = Tag()
                        t.name = tag
                        t.create_by = appuser
                        t.save()
                        entry.tag.add(t)
        entry.path = dirpath
        entry.save()
        # if request.FILES.has_key('file') and number:
        #     # print "OK"
        #     # dirpath += "/image"
        #     mkdir(dirpath+"/image")
        #     updir = dirpath+r'/image/image.zip' #+ form.cleaned_data['title']
        #     destination = open(updir, 'wb+')
        #     upfile = request.FILES['file']
        #     for chunk in upfile.chunks():
        #         destination.write(chunk)
        #     destination.close()
        #     temp_values['files'] = unzip(dirpath+"/image",'image.zip')
        #     # files = os.listdir(dirpath+"/image/")
        #     # for file in files:
        #     #     print file
        # entry.save()
        # return HttpResponseRedirect("/isbooks/category?target=new")
        return HttpResponseRedirect("/isreport/add_entry?id="+str(entry.id))

    else:
        target_year = datetime.datetime.now().strftime("%Y")
        temp_values['authors'] = Author.get_auth_yearth(target_year)
        temp_values['groups'] = Group.group_list()
        temp_values['tags'] = Tag.tag_list()
        if request.GET.has_key('error'):
            error = request.GET['error']
            temp_values['error'] = 1

    temp_values['navi']=get_navi("upload_/isreport/upload-form")
    temp_values['msg'] = msg
    temp_values['target']="upload"
    temp_values['base_title']=u"新規レポート作成ページ"
    temp_values['authors'] = Author.auth_list()
    # temp_values['authors'] = Author.auth_sorted_list()

    # return HttpResponse(t.render(c))
    return render_to_response('isbookshelf/authorized/upload_form.html',temp_values,context_instance=RequestContext(request))

# entry編集
@login_required
def edit_entry(request):
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
    if request.method == 'POST':
        target = request.POST['target']
        name = request.POST['title']
        entry = Entry.get_by_id(int(target))
        if request.POST.has_key('authors'):
            authors = request.POST.getlist('authors')
            entry.author.clear()
            ii = ""
            for auth in authors:
                ii += str(auth)+u","
                au = Author.get_by_id(int(auth))
                if au:
                    entry.author.add(au)
                    au.save()
                # au = Author.get_by_id(int(auth))
                # entry.author.add(au)
                # au.save()
            entry.tmp1 = ii
            # print auth+"OK"
            # entry.img_url = img_url
        if request.POST.has_key('author_list'):
            author_list = request.POST['author_list']
        if request.POST.has_key('tags'):
            tag_list = []
            tags = request.POST['tags']
            tag_list = tags.split(",")
            entry.tag.clear()
            for tag in tag_list:
                if tag:
                    t = Tag.get_by_name(tag)
                    if t:
                        entry.tag.add(t)
                        t.save()
                    else:
                        t = Tag()
                        t.name = tag
                        t.create_by = appuser
                        t.save()
                        entry.tag.add(t)
            # entry.roman = roman
        if request.POST.has_key('groups'):
            groups = request.POST.getlist('groups')
            entry.group.clear()
            for group in groups:
                gr = Group.get_by_id(int(group))
                if gr:
                    entry.group.add(gr)
                    gr.save()

        if request.POST.has_key('abstract'):
            personal = request.POST['abstract']
            entry.abstract = personal
        entry.title = name
        entry.save()
        for auth in reversed(entry.authors()):
            print auth

        # author.save()
        return HttpResponseRedirect("/isreport/add_entry?id="+str(entry.id))

    else:
        if user:
            target = request.GET['target']
            entry = Entry.get_by_id(int(target))
            temp_values = Context()
            temp_values['navi']=get_navi("EntryEdit_/isreport/edit-entry?target="+str(entry.id))
            temp_values['edit_mode'] = True
            temp_values['appuser']=appuser
            temp_values['entry']=entry
            temp_values['authors'] = Author.auth_list()
            temp_values['groups'] = Group.group_list()
            temp_values['tags'] = Tag.tag_list()
            temp_values['base_title']=entry.title+u" 編集ページ"
            return render_to_response('isbookshelf/authorized/upload_form.html',temp_values,
                    context_instance=RequestContext(request))

@login_required
def EditEntryPage(request):
    msg = ''
    isdraft = ""
    islang = ""
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
        # return HttpResponseRedirect("/isreport/forbidden")
        raise Http403
    if request.GET.has_key('id'):
        entry = Entry.get_by_id(request.GET['id'])
    elif request.POST.has_key('id'):
        entry = Entry.get_by_id(request.POST['id'])
    else:
        # return HttpResponseRedirect("/isreport/notfound")
        raise Http404
    temp_values['target']="upload"
    temp_values['entry'] = entry
    temp_values['appuser'] = appuser
    if entry.upload_by.nickname == u"api":
        temp_values['isstyle'] = True
    if request.POST.has_key('isdraft'):
        isdraft = request.POST['isdraft']
    if request.POST.has_key('istranslate'):
        islang = request.POST['istranslate']
    if request.POST.has_key('isstyle'):
        isstyle = True
    dirpath = entry.path
    if request.method == 'POST':
        # print "POST"
        org = request.POST['soups']
        soups = request.POST['html_body']
        soups_def = request.POST['html_body_def']
        # print soups
        t_content = loader.get_template('isbookshelf/component/preview_html.html')
        c_content = Context()
        c_content['pub_year'] = entry.publish.strftime("%Y")
        c_content['title'] = entry.title
        c_content['html'] = soups_def

        soup_text = HttpResponse(t_content.render(c_content)).content
        analyze = Analyze()
        result = dict()
        # if True:
        try:
            # result = analyze.gets(soup_text)
            content_main = analyze.content_gets(soup_text)
            # 本文をデータベースに保存
            entry.content = str(content_main)
            # print content_main
            msg = content_main
        except:
            pass
        c_content['html'] = soups
        paths = JAM_DIR + dirpath
        form = UploadFileForm(request.POST, request.FILES)
        if request.FILES.has_key('pdf'):
            upfile = request.FILES['pdf']
            destination = open(JAM_DIR + dirpath+"/isreport"+entry.num+".pdf", 'wb+')
            for chunk in upfile.chunks():
                destination.write(chunk)
            destination.close()
        if request.POST.has_key('istext'):
            entry.istext = True
        else:
            entry.istext = False
        if request.POST.has_key('ispdf'):
            entry.ispdf = True
        else:
            entry.ispdf = False

        if isstyle:
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
        if isdraft or islang:
            if islang:
                from parsee import *
                if True:
                    p_title = entry.title.encode("utf-8")
                    p_abst = entry.abstract.encode("utf-8")
                    p_body = org.encode("utf-8")
                    # htmls = open(p_body).read()
                    parse = Parsee()
                    # parse.html = p_body
                    # t1 = time.time()
                    e_title = parse.parse(p_title)
                    e_abst = parse.parse(p_abst)
                    e_body = parse.parse(p_body)

                    e_entry = Entry()
                    e_entry.title = e_title
                    e_entry.abstract = e_abst
                    # entry.section = section
                    e_entry.num = str(datetime.datetime.now().year)+str(appuser.get_ids())+str(appuser.get_numbers())
                    e_entry.publish = entry.publish
                    e_entry.upload_by = appuser
                    e_entry.ispublic = entry.ispublic
                    if True:
                        dirpath = ""
                        if not e_entry.ispublic:
                            dirpath = "private"
                            mkdir(JAM_DIR + dirpath)
                            dirpath += "/"
                        # dirpath = JAM_DIR
                        # dirpath = r'/Library/WebServer/Documents/isbooks/'
                        dirpath += str(e_entry.publish.year)
                        mkdir(JAM_DIR + dirpath)
                        dirpath += "/"
                        dirpath += str(e_entry.publish.month)
                        mkdir(JAM_DIR + dirpath)
                        dirpath += "/"
                        dirpath += str(e_entry.publish.day)
                        mkdir(JAM_DIR + dirpath)
                        dirpath += "/"
                        dirpath += str(e_entry.num)
                        mkdir(JAM_DIR + dirpath)
                        set_static(JAM_DIR + dirpath)
                    e_entry.path = dirpath
                    e_entry.save()
                    for i in entry.authors():
                        e_entry.author.add(i)
                    e_entry.lang = 2
                    e_entry.tmp1 = entry.tmp1
                    e_entry.save()
                    org_html = open(JAM_DIR + dirpath+"/indexorg.html", "wb+")
                    org_html.write(e_body.encode("utf-8"))
                    org_html.close
                    return HttpResponseRedirect("/isreport/add_entry?id="+str(e_entry.id))
                # except:
                #     pass
            else:
                entry.isdraft = True
        else:
            entry.isdraft = False
            # アップロード時に単体のepubテンプレートを設置しておく。本文編集時に同時に更新する
            # epub自体はダウンロード時に動的に生成する。生成時に生じるシェルスクリプトの時間差によりこの方法以外不可？
            entries = []
            entries.append(entry)
            book = None
            book_id = "isreport"+str(entry.num)
            dirpath = JAM_DIR + dirpath
            set_template(dirpath)
            tmp_html = open(paths+"/OEBPS/chap01.xhtml", "wb+")
            tmp_html.write(HttpResponse(t_content.render(c_content)).content)
            tmp_html.close
            file_list = os.listdir(paths)
            #for flist in file_list:
                #print flist
            mvstatics(paths,paths+u"/OEBPS","images")
            # mvstatics(paths,paths+u"/OEBPS","images")
            # mvstatics(paths,paths+u"/OEBPS","image")

            e_title = entry.title
            e_creater = ""
            for author in entry.author.all():
                e_creater += author.roman+","
            e_bookid = book_id
            e_publisher = u"IS"
            e_list = []
            count = 1
            for entry in entries:
                coun = ""
                if count < 10:
                    coun = u"0"+str(count)
                else:
                    coun = str(count)
                item = Context()
                item['id'] = entry.id
                item['ref'] = u"chap"+coun+u".xhtml"
                item['title'] = entry.title
                item['entry'] = entry
                e_list.append(item)
                count +=1
            e_author = e_creater
            e_own_page = "http://is.doshisha.ac.jp/isreport/"
            e_own_name = "IS Group"
            ss=""
            t_content = loader.get_template('isbookshelf/oebps/content.opf')
            c_content = Context()
            c_content['title'] = e_title
            c_content['creater'] = e_creater
            c_content['bookid'] = e_bookid
            c_content['publisher'] = e_publisher
            c_content['list'] = e_list

            o_content = open(dirpath+"/OEBPS/content.opf", "w")
            o_content.write(HttpResponse(t_content.render(c_content)).content)
            o_content.close

            t_title = loader.get_template('isbookshelf/oebps/title_page.xhtml')
            c_title = Context()
            c_title['title'] = e_title
            c_title['author'] = e_author
            c_title['publisher'] = e_publisher
            c_title['own_page'] = e_own_page
            c_title['own_name'] = e_own_name

            o_title = open(dirpath+"/OEBPS/title_page.xhtml", "w")
            o_title.write(HttpResponse(t_title.render(c_title)).content)
            o_title.close

            t_agenda = loader.get_template('isbookshelf/oebps/agenda.xhtml')
            c_agenda = Context()
            c_agenda['list'] = e_list

            o_agenda = open(dirpath+"/OEBPS/agenda.xhtml", "w")
            o_agenda.write(HttpResponse(t_agenda.render(c_agenda)).content)
            o_agenda.close

            t_toc = loader.get_template('isbookshelf/oebps/toc.ncx')
            c_toc = Context()
            c_toc['title'] = e_title
            c_toc['bookid'] = e_bookid
            c_toc['list'] = e_list

            o_toc = open(dirpath+"/OEBPS/toc.ncx", "w")
            o_toc.write(HttpResponse(t_toc.render(c_toc)).content)
            o_toc.close
            if entry.approval:
                t_rss = loader.get_template('isbookshelf/static/rss_temp.xml')
                c_rss = Context()
                c_rss['items'] = Entry.get_rss(SEARCH_SPAN)
                c_rss['lastitem'] = Entry.get_latest()
                c_rss['domain'] = DOMAIN
                o_rss = open(STATIC_DIR+'isbookshelf/templates/isbookshelf/static/rss.xml', "w")
            # htmls = HttpResponse(t_rss.render(c_rss)).content
            # print "####"+htmls
            # htmls = htmls.replace('src="/report/'+entry.path+'/','')
                if not DEBUG:
                    o_rss.write(HttpResponse(t_rss.render(c_rss)).content)
                o_rss.close
        if not request.POST.has_key('istext'):
            if not request.POST.has_key('ispdf'):
                entry.isdraft = True
        entry.save()
        # return HttpResponse(msg)
        return HttpResponseRedirect("/isreport/entry/"+str(entry.id))
    else:
        org = ""
        try:
            # ファイル読み込み。前回のがあれば読み込む。なければ新規作成
            f = open(JAM_DIR + dirpath+"/indexorg.html")
            org = f.read() # 読み込む(改行文字も含まれる)
            # while line:
            #     org += line
            #     #print line
            #     line = f.readline()
        except:
            pass
        pdftitle = ""
        file_list = os.listdir(JAM_DIR + dirpath)
        for lis in file_list:
            lists = lis.split(".")
            if len(lists)>1:
                if lists[1] =="pdf":
                    pdftitle = lis
        temp_values['pdftitle'] = pdftitle
        temp_values['navi']=get_navi("Upload_/isreport/upload-form")
        temp_values['target']="upload"
        temp_values['base_title']=entry.title+u" 編集ページ"
        if org:
            temp_values['orgs'] = org
        return render_to_response('isbookshelf/authorized/upload_editor.html',
                temp_values,context_instance=RequestContext(request))

# dashboardページ
@login_required
def DashboardPage(request):
    user = None
    appuser = None
    tar = "Dashboard_/isreport/dashboard"
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
        page=1
        if request.GET.has_key('page'):
            page = int(request.GET['page'])
            tar += ",page"+str(page)+"_/isreport/dashboard?page="+str(page)
        entries,entry_count = Entry.get_my_reports(appuser,page)
        temp_values = Context()
        page_list,pages = get_page_list(page, entry_count, 10)
        temp_values['page_list']=page_list
        temp_values['pages']=pages
        temp_values['navi']=get_navi(tar)
        # temp_values['new_items']=new_item()
        temp_values['target_url']='dashboard'
        temp_values['target']="dashboard"
        temp_values['appuser']=appuser
        temp_values['items']=entries
        temp_values['base_title']=u"Dashboard"

        return render_to_response('isbookshelf/authorized/dashboard.html',temp_values,
                    context_instance=RequestContext(request))
    # else:
    #     return HttpResponseRedirect("/isreport/forbidden")

# レポート承認ページ
@login_required
def ApprovalPage(request):
    user = None
    appuser = None
    issuper = False
    para = ""
    tar = "Approval_/isreport/approval"
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
        if request.GET.has_key('isdraft'):
            if user.is_superuser:
                issuper = True
                para = "isdraft=true"
        if True:
            if request.GET.has_key('target'):
                target_id = request.GET['target']
                target = Entry.get_by_id(int(target_id))
                if target and user.is_staff:
                    if request.GET.has_key('deny'):
                        target.approval = False
                    else:
                        target.approval = True
                    target.save()
                    try:
                        t_rss = loader.get_template('isbookshelf/static/rss_temp.xml')
                        c_rss = Context()
                        c_rss['items'] = Entry.get_rss(SEARCH_SPAN)
                        c_rss['lastitem'] = Entry.get_latest()
                        c_rss['domain'] = DOMAIN
                        o_rss = open(STATIC_DIR+'/isbookshelf/templates/isbookshelf/static/rss.xml', "w")
                        if not DEBUG:
                            o_rss.write(HttpResponse(t_rss.render(c_rss)).content)
                        o_rss.close
                    except:
                        pass
            page=1
            if request.GET.has_key('page'):
                page = int(request.GET['page'])
                tar += ",page"+str(page)+"_/isreport/approval?page="+str(page)+"&"+para
            entries,entry_count = Entry.get_approvals(page,issuper)
            temp_values = Context()
            page_list,pages = get_page_list(page, entry_count, 10)
            temp_values['target_url']='approval'
            temp_values['page_list']=page_list
            temp_values['pages']=pages
            temp_values['navi']=get_navi(tar)
            # temp_values['new_items']=new_item()
            temp_values['target']="approval"
            temp_values['appuser']=appuser
            temp_values['items']=entries
            temp_values['base_title']=u"レポート承認ページ"
            temp_values['para']=para
            return render_to_response('isbookshelf/authorized/approval.html',temp_values,
                    context_instance=RequestContext(request))
        else:
            # return HttpResponseRedirect("/isreport/notfound")
            raise Http404
    else:
        # return HttpResponseRedirect("/isreport/forbidden")
        raise Http403

# settingページ
@login_required
def SettingPage(request):
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
        favorites = FavoriteHandler.get_by_appuser(appuser)
        temp_years = []
        now_year = int(datetime.datetime.now().strftime("%Y"))
        for ye in xrange(openning_year, now_year+1):
            temp_years.append(str(ye))
        redirect = "setting"
        if request.method == 'GET':
            if request.GET.has_key('is_first'):
                redirect = ""
        else:
            print request.POST
            if request.POST.has_key('is_first'):
                redirect = ""
            setting_author = ""
            setting_roman = ""
            setting_year = []
            setting_intro = ""
            setting_yearth = 0
            setting_img = ""
            author = None
            years = ""
            if request.POST.has_key('setting_author'):
                setting_author = request.POST['setting_author']
                try:
                    author = Author.get_by_id(int(setting_author))
                    old_author = Author.get_by_user(appuser)
                except:
                    pass
            if request.POST.has_key('setting_roman'):
                setting_roman = request.POST['setting_roman']
            if request.POST.has_key('setting_year'):
                setting_year = request.POST.getlist('setting_year')
                if setting_year[0]!="0":
                    setting_yearth = int(setting_year[0])-openning_year
                for ye in setting_year:
                    years += ye +","
            if author:
                author.roman = setting_roman
                try:
                    old_author.user = None
                    old_author.save()
                except:
                    pass
                author.user = appuser
                if request.POST.has_key('setting_img'):
                    setting_img = request.POST['setting_img']
                    author.img_url = setting_img
                if request.POST.has_key('setting_intro'):
                    setting_intro = request.POST['setting_intro']
                    author.personal = setting_intro
                if years:
                    author.year = years
                if setting_yearth:
                    author.yearth = setting_yearth
                author.save()
                # name = models.CharField(max_length=100)
                # roman = models.CharField(max_length=100)
                # user = models.ForeignKey(ApplicationUser,blank=True, null=True)
                # create_at = models.DateTimeField(auto_now_add=True)
                # update_at = models.DateTimeField(auto_now=True)
                # personal = models.TextField(max_length = 1000, blank=True, null=True)
                # img_url = models.CharField(max_length = 100, blank=True, null=True)
                # isvalid = models.BooleanField(default=True)
                # # year = models.IntegerField(default=0)
                # year = models.CharField(max_length = 100, blank=True, null=True)
                # rank = models.CharField(max_length = 30, default="etc")
                return HttpResponseRedirect("/isreport/"+redirect)

        temp_values = Context()
        # temp_values['date']=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M")
        temp_values['is_first']=redirect
        temp_values['years']=temp_years
        temp_values['navi']=get_navi("Setting_/isreport/setting")
        # temp_values['new_items']=new_item()
        temp_values['target']="setting"
        temp_values['appuser']=appuser
        temp_values['favorites']=favorites
        temp_values['authors']=Author.auth_sorted_list()
        temp_values['base_title']="Setting"
        return render_to_response('isbookshelf/authorized/setting.html',temp_values,
                    context_instance=RequestContext(request))
    # else:
    #     return HttpResponseRedirect("/isreport/forbidden")
