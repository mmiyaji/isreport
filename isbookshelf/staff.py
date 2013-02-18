#!/usr/bin/env python
# encoding: utf-8
"""
staff.py

Created by Masahiro MIYAJI on 2011-05-10.
Copyright (c) 2011 ISDL. All rights reserved.
"""

from views import *
from django.contrib.auth.decorators import login_required
import sys
try:
    sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/")
    import MeCab
except:
    pass
import os,re
import operator
def to_int(value, default=None):
    try:
        i = int(value)
        return True
    except:
        return False
def parse(texts,t,ignones,words,markov):
    _data = t.parse(texts)
    # print _data
    lines = _data.split(os.linesep)
    w1 = ""
    w2 = ""
    for row in lines:
        try:
            word_hinshi = row.split(",")[0]
            word,hinshi = word_hinshi.split("\t")
            if hinshi == '名詞':
                # print word_hinshi
                if to_int(word):
                    continue
                if word in ignones:
                    continue
                if not words.has_key(word):
                    words[word] = 0
                words[word] += 1
                if w1 and w2:
                    if (w1, w2) not in markov:
                        markov[(w1, w2)] = 0
                    markov[(w1, w2)] +=1
                w1, w2 = w2, word
        except:
            pass
    items = words.items()
    return items,words,markov
# shell
@login_required
def Shell(request):
    user = None
    appuser = None
    t = MeCab.Tagger("mecabrc")
    ignones = [".","．","-","(",")","/"]
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
    p1 = re.compile(u'<.*?>')
    p2 = re.compile(u'{=.*?=}')
    p3 = re.compile(u'{{.*?}}')
    texts = """Lorem ipsum dolor sit amet, consectetur adipisicing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    entries = new_item(span=2000)
    all_items = []
    all_result = ""
    words = {}
    markov = {}
    for entry in entries:
        print entry.title
        result = ""
        # texts = entry.title.encode("utf-8")
        texts = entry.title.encode("utf-8")
        texts = p1.sub('', texts)
        texts = p2.sub('', texts)
        texts = p3.sub('', texts)
        # print texts
        items,words,markov = parse(texts,t,ignones,words,markov)
        all_items.extend(items)
        texts = entry.abstract.encode("utf-8")
        texts = p1.sub('', texts)
        texts = p2.sub('', texts)
        texts = p3.sub('', texts)
        # print texts
        items,words,markov = parse(texts,t,ignones,words,markov)
        all_items.extend(items)
        # for w,c in items:
        #     # print "%d:%s\t%d" % (len(w),w,c)
        #     result += "%s\t%d\n" % (w,c)
    result += "\n\n\n"
    items = words.items()
    items.sort(key=operator.itemgetter(1), reverse=True)
    count = 0
    markov_items = markov.items()
    markov_items.sort(key=operator.itemgetter(1), reverse=True)
    # markov_items.sort(key=operator.itemgetter(0), reverse=True)
    for w,c in markov_items:
        count +=1
        all_result += "%d:[%s,%s]\t%d\n<br />" % (count,w[0],w[1],c)
        print "%d:[%s,%s]\t%d" % (count,w[0],w[1],c)
    # for w,c in items:
    #     count +=1
    #     all_result += "%d:%s\t%d\n<br />" % (count,w,c)
    #     print "%d:%s\t%d" % (count,w,c)
    return HttpResponse(all_result)
# お知らせ編集
@login_required
def edit_renew(request):
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
    else:
        # return HttpResponseRedirect("/isreport/forbidden")
        raise Http403
    if request.method == 'POST':
        if request.POST.has_key('top_soup'):
            top_soup = request.POST['top_soup']
            t_soup = open(STATIC_DIR+'/isbookshelf/templates/isbookshelf/static/top_renew.html', "w")
            t_soup.write(top_soup.encode('utf-8'))
            t_soup.close
        if request.POST.has_key('soup'):
            soup = request.POST['soup']
            m_soup = open(STATIC_DIR+'/isbookshelf/templates/isbookshelf/static/renew.html', "w")
            m_soup.write(soup.encode('utf-8'))
            m_soup.close
        return HttpResponseRedirect("/isreport")
    else:
        temp_values = Context()
        temp_values['navi']=get_navi("Renew_/isreport/renew,RenewEdit_/isreport/edit-renew")
        temp_values['target']="renew"
        temp_values['appuser']=appuser
        temp_values['base_title']=u"更新履歴編集"
        return render_to_response('isbookshelf/staff/edit_renew.html',temp_values,
                    context_instance=RequestContext(request))

# group編集
@login_required
def edit_group(request):
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
    if request.method == 'POST':
        target = request.POST['target']
        name = request.POST['name']
        group = Group.get_by_id(int(target))
        if request.POST.has_key('img_url'):
            img_url = request.POST['img_url']
            if img_url=="http://":
                img_url=""
            group.img_url = img_url
        if request.POST.has_key('personal'):
            personal = request.POST['personal']
            group.personal = personal
        group.name = name
        group.save()
        return HttpResponseRedirect("/isreport/group/")

    else:
        target = request.GET['target']
        group = Group.get_by_id(int(target))
        temp_values = Context()
        temp_values['navi']=get_navi("GroupEdit_/isreport/edit-group?target="+target)
        temp_values['appuser']=appuser
        temp_values['group']=group

        return render_to_response('isbookshelf/staff/edit_group.html',temp_values,
                    context_instance=RequestContext(request))

# author編集
@login_required
def edit_author(request):
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)

    if request.method == 'POST':
        if user.is_staff:
            target = request.POST['target']
            name = request.POST['name']
            author = Author.get_by_id(int(target))
            if request.POST.has_key('img_url'):
                img_url = request.POST['img_url']
                if img_url=="http://":
                    img_url=""
                author.img_url = img_url
            if request.POST.has_key('roman'):
                roman = request.POST['roman']
                author.roman = roman
            if request.POST.has_key('personal'):
                personal = request.POST['personal']
                author.personal = personal
            setting_year = []
            years = ""
            setting_yearth = 0
            if request.POST.has_key('setting_year'):
                setting_year = request.POST.getlist('setting_year')
                if setting_year[0]!="0":
                    setting_yearth = int(setting_year[0])-openning_year
                for ye in setting_year:
                    years += ye +","

            author.rank = request.POST['authorpost']
            author.year = years
            author.yearth = setting_yearth
            author.name = name
            author.save()
            return HttpResponseRedirect("/isreport/author?active=true")

    else:
        temp_values = Context()
        temp_years = []
        now_year = int(datetime.datetime.now().strftime("%Y"))
        for ye in xrange(openning_year, now_year+1):
            temp_years.append(str(ye))
        temp_values['years']=temp_years
        target = request.GET['target']
        author = Author.get_by_id(int(target))
        temp_values['navi']=get_navi("AuthorEdit_/isreport/edit-author?target="+target)
        temp_values['appuser']=appuser
        temp_values['author']=author
        # temp_values['authors'] = Author.auth_list()
        return render_to_response('isbookshelf/staff/edit_author.html',temp_values,
                    context_instance=RequestContext(request))

# tag編集
@login_required
def edit_tag(request):
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)

    if request.method == 'POST':
        # if user.is_staff:
        if request.POST['name'] and request.POST['target']:
            target = request.POST['target']
            name = request.POST['name']
            tag = Tag.get_by_id(int(target))
            # if request.POST.has_key('img_url'):
            #     img_url = request.POST['img_url']
            #     if img_url=="http://":
            #         img_url=""
            #     author.img_url = img_url
            # if request.POST.has_key('roman'):
            #     roman = request.POST['roman']
            #     author.roman = roman
            if request.POST.has_key('personal'):
                personal = request.POST['personal']
                tag.description = personal

            # setting_year = []
            # years = ""
            # setting_yearth = 0
            # if request.POST.has_key('setting_year'):
            #     setting_year = request.POST.getlist('setting_year')
            #     if setting_year[0]!="0":
            #         setting_yearth = int(setting_year[0])-openning_year
            #     for ye in setting_year:
            #         years += ye +","
            #
            # author.rank = request.POST['authorpost']
            # author.year = years
            # author.yearth = setting_yearth
            tag.name = name
            tag.save()
            return HttpResponseRedirect("/isreport/tag/"+name)

    else:
        temp_values = Context()
        # temp_years = []
        # now_year = int(datetime.datetime.now().strftime("%Y"))
        # for ye in xrange(openning_year, now_year+1):
        #     temp_years.append(str(ye))
        # temp_values['years']=temp_years
        target = request.GET['target']
        tag = Tag.get_by_id(int(target))
        temp_values['navi']=get_navi("TagEdit_/isreport/edit-tag?target="+target)
        temp_values['appuser']=appuser
        temp_values['tag']=tag
        # temp_values['authors'] = Author.auth_list()
        return render_to_response('isbookshelf/staff/edit_tag.html',temp_values,
                    context_instance=RequestContext(request))

# keyword編集
@login_required
def edit_keyword(request):
    user = None
    appuser = None
    if request.user.is_authenticated():
        user = request.user
        appuser = ApplicationUser.get_by_user(user)
    if request.method == 'POST':
        if request.POST['name'] and request.POST['target']:
            target = request.POST['target']
            name = request.POST['name']
            view_level = int(request.POST['view_level'])
            tag = Word.get_by_id(int(target))
            if request.POST.has_key('personal'):
                personal = request.POST['personal']
                tag.description = personal
            tag.name = name
            tag.view_level = view_level
            tag.save()
            return HttpResponseRedirect("/isreport/keyword/"+name)
    else:
        temp_values = Context()
        target = request.GET['target']
        tag = Word.get_by_id(int(target))
        temp_values['navi']=get_navi("KeywordEdit_/isreport/edit-keyword?target="+target)
        temp_values['appuser']=appuser
        temp_values['tag']=tag
        return render_to_response('isbookshelf/staff/edit_keyword.html',temp_values,
                    context_instance=RequestContext(request))

# group作成
@login_required
def create_group(request):
    try:
        name = ""
        img_url = ""
        personal = ""
        if request.POST.has_key('name'):
            name = request.POST['name']
        if request.POST.has_key('img_url'):
            img_url = request.POST['img_url']
            if img_url=="http://":
                img_url=""
        if request.POST.has_key('personal'):
            personal = request.POST['personal']
        if len(name) < 1:
            raise Http404
            # return HttpResponseRedirect("/isreport/notfound")
        if Group.objects.filter(name=name):
            raise Http404
            # return HttpResponseRedirect("/isreport/notfound")
        else:
            user = None
            appuser = None
            if request.user.is_staff:
                user = request.user
                appuser = ApplicationUser.get_by_user(user)
                group = Group()
                group.create_by = appuser
                group.name = name
                group.img_url = img_url
                group.personal = personal
                group.save()
            return HttpResponseRedirect('/isreport/group/')
        # return HttpResponseRedirect("/isreport/forbidden")
        # raise Http403
    except:
        raise Http403
        # return HttpResponseRedirect("/isreport/forbidden")
        # error = "Sorry. Can't use this account"
        # return render_to_response('entries/registration/login.html',
        #                               {'loginError':error},
        #                               context_instance=RequestContext(request))

# author作成
@login_required
def create_author(request):
    if True:
        if request.POST.has_key('name'):
            name = request.POST['name']
        if request.POST.has_key('roman'):
            roman = request.POST['roman']
        post = request.POST['authorpost']
        if request.POST.has_key('img_url'):
            img_url = request.POST['img_url']
            if img_url=="http://":
                img_url=""
        personal = request.POST['personal']
        setting_year = []
        years = ""
        setting_yearth = 0
        if request.POST.has_key('setting_year'):
            setting_year = request.POST.getlist('setting_year')
            if setting_year[0]!="0":
                setting_yearth = int(setting_year[0])-openning_year
            for ye in setting_year:
                years += ye +","
        if len(name) < 1:
            raise Http404
            # return HttpResponseRedirect("/isreport/notfound")
        if Author.objects.filter(name=name):
            raise Http404
            # return HttpResponseRedirect("/isreport/notfound")
        else:
            user = None
            appuser = None
            if request.user.is_staff:
                user = request.user
                appuser = ApplicationUser.get_by_user(user)

                author = Author()
                author.create_by = appuser
                author.name = name
                author.roman = roman
                author.rank = post
                author.img_url = img_url
                author.personal = personal
                author.year = years
                author.yearth = setting_yearth
                author.save()
            return HttpResponseRedirect('/isreport/author?active=true')
    # except:
    #     raise Http403
        # return HttpResponseRedirect("/isreport/forbidden")
        # error = "Sorry. Can't use this account"
        # return render_to_response('entries/registration/login.html',
        #                               {'loginError':error},
        #                               context_instance=RequestContext(request))
