# -*- coding: utf-8 -*-
import hashlib,logging
# 研究室開始年度？あってるか分かりませんが
openning_year = 1996
SEARCH_SPAN = 25
NEW_SPAN = 15
TAG_SPAN = 100
KEYWORD_SPAN = 100
GROUP_SPAN = 15
APP_USER = "ismember"
# MISLのbasic認証
APP_PASSWD = ""
# MAYのaminパスと同じ
ADMIN_PASS = ""
DOCUMENT_DIR = r"/var/www"
USER_DIR = r"/var/www/strage/users"
STRAGE_DIR = r"isbookshelf/strage"
BASE_DIR = r"/home/mmiyaji/isapps"
STATIC_DIR = r"/home/mmiyaji/isapps/isbooks/"
JAM_DIR = r'/var/www/report/'
DOMAIN = u"http://is.doshisha.ac.jp"
try:
    from settings_local import *
except:
    pass
def guts():
    from isbookshelf.models import *
    from isbookshelf.soup import *
    f = open("ispaths.txt")
    line = f.readline()
    array = []
    items = Entry.objects.all().filter(isdraft=False).filter(isvalid=True)
    for item in items:
        if not item.content:
            path = "/home/mmiyaji/report/"+item.path.strip()+"/index.html"
            print item.title.strip(),":",path
            try:
                res = mains(path)
                print res
                if res:
                    item.content = res
                    item.save()
            except:
                print "error"
    # while line:
    #     tmp = line.split("//,")
    #     array.append([tmp[0].strip(),tmp[1].strip()])
    #     line = f.readline()

def flame():
    from isbooks.isbookshelf.models import *
    array = []
    items = Entry.objects.all().filter(isdraft=False).filter(isvalid=True)
    for item in items:
        if item.content:
            # path = "/home/mmiyaji/report/"+item.path.strip()+"/index.html"
            print item.title.strip()
            try:
                res = item.content
                res = res.replace('src="images/','src="/report/'+item.path.strip()+'/images/')
                if res:
                    item.content = res
                    item.save()
            except:
                print "error"

def create_hash(string):
    return hashlib.md5(str(string)).hexdigest()

def get_navi(target=""):
    # <li class="active"><a href="/">Home</a></li>
    if target:
        result = "<li><a href='/isreport'>Home</a></li>"
    else:
        result = "<li class='active'><a href='/isreport'>Home</a></li>"
        return result
    try:
        tar = target.split(",")
        for c,t in enumerate(tar):
            # result +=  " &gt;&gt; ";
            if c==len(tar)-1:
                result += "<li class='active'><a href='"+t.split("_")[1].replace(u"-",u"_").replace(" ","%20")+"'>"+t.split("_")[0].title()+"</a></li>"
            else:
                result += "<li><a href='"+t.split("_")[1].replace(u"-",u"_").replace(" ","%20")+"'>"+t.split("_")[0].title()+"</a></li>"
        return result
    except:
        return result

def get_page_list(page, count, search_span):
    pages = dict()
    page_max = (count / search_span)
    if count%search_span!=0:
        page_max +=1
    pre_page = None
    next_page = None
    if page_max >= page+1:
        next_page = page+1
    if page!=0:
        pre_page = page-1
    pages['next_page'] = next_page
    pages['now_page'] = page
    pages['pre_page'] = pre_page
    pages['max'] = count
    pages['start'] = (page-1)*search_span+1
    end = 0
    if (page)*search_span>=count:
        end=count
    else:
        end = (page)*search_span
    pages['end'] = end
    page_list = []
    if page_max>15:
        page_list.append(1)
        mins = page-5
        maxs = page+6
        if mins<2:
            mins = 2
            maxs = 13
        # else:
            # page_list.append("-")
        if maxs>page_max:
            maxs = page_max
        for x in range(mins, maxs):
            page_list.append(x)
        # else:
        #     for x in range(mins, maxs):
        #         page_list.append(x)
            # page_list.append("-")
        page_list.append(page_max)
    else:
        for x in range(1, page_max+1):
            page_list.append(x)
        if len(page_list)==1:
            page_list = None
    return page_list,pages
