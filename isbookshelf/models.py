# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import simplejson
# from isbooks.settings import *
# from isnetwork.models import *
# from isbookshelf.models import *
# from isrecommend.models import *
from isbookshelf.models import *
from utils import *
import datetime,time,math
import urllib
from django.db.models import Q
from django.core.cache import cache

class Book(models.Model):
    title = models.CharField(max_length = 255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(auto_now_add=True)
    view_auth = models.BooleanField(default=True)
    change_auth = models.BooleanField(default=True)
    isvalid = models.BooleanField(default=True)
    description = models.TextField(default="", max_length = 1000, blank=True, null=True)
    # path = models.CharField(max_length = 100)
    tmp1 = models.CharField(max_length = 30, default="", blank=True, null=True)
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)

    @staticmethod
    def get_books(page=0):
        if page!=0:
            page = page*10 - 10
        endpage = page + 10
        result = Book.objects.order_by('-update_at').filter(isvalid=True)[page:endpage]
        return result

    @staticmethod
    def get_count():
        return Book.objects.filter(isvalid=True).count()

    @staticmethod
    def get_by_id(keyid):
        result=None
        try:
            result = Book.objects.get(id__exact=keyid)
        except:
            result = None
        return result

    def show_update_at(self):
        date = self.update_at
        return date.strftime("%Y .%m .%d")

    def get_owner(self):
        bh = BookHandler.get_by_book(self)
        return bh.create_by

    def get_subs(self):
        return BookHandler.get_by_book(self)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id
    # class Meta:
    #     order_with_respect_to = 'question'

class Favorite(models.Model):
    memo = models.TextField(max_length = 1000, blank=True, null=True)

    def __unicode__(self):
        return self.memo

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id
    # class Meta:
    #     order_with_respect_to = 'question'

class ApplicationUser(models.Model):
    user = models.ForeignKey(auth_models.User, db_index=True)
    userid = models.IntegerField(default=0)
    nickname = models.CharField(max_length=255)
    personal = models.TextField(max_length = 1000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    year = models.IntegerField(default=2000)
    roll = models.CharField(max_length=10,default="user")
    isvalid = models.BooleanField(default=True)
    books = models.ManyToManyField(Book, blank=True, null=True)
    favorites = models.ManyToManyField(Favorite, blank=True, null=True)
    tmp1 = models.CharField(max_length = 30, default="", blank=True, null=True)
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)

    def get_books(self):
        return self.books.all().order_by('-update_at')

    def favorites(self):
        return self.favorites.all()

    def get_auth(self):
        return Author.get_by_user(self)

    def get_ids(self):
        author = Author.get_by_user(self)
        if author:
            return author.get_ids()
        else:
            return None
        # nums = int(self.id)
        # number = ""
        # if nums<100:
        #     number += "0"
        #     if nums<10:
        #         number += "0"
        # number += str(nums+1)
        # return number

    def get_numbers(self):
        author = Author.get_by_user(self)
        if author:
            return author.get_numbers()
        else:
            return None

    def approval_coount(self):
        return Entry.get_approvals_count()
    @staticmethod
    def get_by_name(name=""):
        result=None
        try:
            result = ApplicationUser.objects.filter(nickname=name).get()
        except:
            result = None
        return result

    @staticmethod
    def get_by_user(user):
        if ApplicationUser.objects.filter(user=user).count()>0:
            return ApplicationUser.objects.filter(user=user).get()
        else:
            return None

    def __unicode__(self):
        return self.nickname

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id


class Author(models.Model):
    name = models.CharField(max_length=255)
    roman = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(ApplicationUser,blank=True, null=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True, db_index=True)
    update_at = models.DateTimeField(auto_now=True, db_index=True)
    personal = models.TextField(max_length = 1000, blank=True, null=True)
    personal_link = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.CharField(max_length = 255, blank=True, null=True)
    isvalid = models.BooleanField(default=True)
    # year = models.IntegerField(default=0)
    year = models.CharField(max_length = 100, blank=True, null=True, db_index=True)
    yearth = models.IntegerField(default=0, db_index=True)
    rank = models.CharField(max_length = 30, default="etc", db_index=True)
    tmp1 = models.CharField(max_length = 30, default="", blank=True, null=True)
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)


    def enc_name(self):
        return urllib.quote(self.name.encode('utf-8'))

    def get_years(self):
        if self.year:
            return self.year.split(",")
        else:
            return None

    def get_rank(self):
        if self.rank =="etc":
            return u"研究員"
        elif self.rank =="ob":
            return u"OB / OG"
        elif self.rank =="prof":
            return u"教員"
        elif self.rank =="doc":
            return u"博士課程後期"
        elif self.rank =="m2":
            return u"修士2年"
        elif self.rank =="m1":
            return u"修士1年"
        elif self.rank =="u4":
            return u"学部4年"
        elif self.rank =="etc":
            return u"研究員"


    def get_ids(self):
        nums = int(self.id)
        number = ""
        if nums<100:
            number += "0"
            if nums<10:
                number += "0"
        number += str(nums+1)
        return number

    def get_numbers(self):
        nums = int(Entry.get_numbers(self))
        number = ""
        if nums<100:
            number += "0"
            if nums<10:
                number += "0"
        number += str(nums+1)
        return number

    @staticmethod
    def get_auth_yearth(year):
        result=None
        try:
            result = Author.objects.filter(year__contains=year)
        except:
            result = None
        return result

    @staticmethod
    def get_auth_year(year):
        result=None
        try:
            result = Author.objects.filter(yearth__exact=year)
        except:
            result = None
        return result


    @staticmethod
    def get_by_id(keyid):
        result=None
        try:
            result = Author.objects.get(id__exact=keyid)
        except:
            result = None
        return result

    @staticmethod
    def auth_list():
        return Author.objects.all()

    @staticmethod
    def auth_sorted_list():
        return Author.objects.order_by('-yearth')

    @staticmethod
    def get_by_name(name=""):
        result=None
        try:
            result = Author.objects.filter(name=name).get()
        except:
            result = None
        return result

    @staticmethod
    def get_by_s_name(name=""):
        result=None
        try:
            result = Author.objects.filter(name__contains=name).get()
        except:
            result = None
        return result

    @staticmethod
    def get_by_user(user):
        if Author.objects.filter(user=user).count()>0:
            return Author.objects.filter(user=user).get()
        else:
            return None

    def __unicode__(self):
        year = ""
        if self.yearth==0:
            year = u"教授"
        else:
            year = str(self.yearth)+u"th"
        result = self.name+u" : "+year
        return result

    def get_absolute_url(self):
        return "/isreport/author/%s" % self.name

class Group(models.Model):
    name = models.CharField(max_length=255)
    roman = models.CharField(max_length=255, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    personal = models.TextField(max_length = 1000, blank=True, null=True)
    img_url = models.CharField(max_length = 255, blank=True, null=True)
    isvalid = models.BooleanField(default=True)
    create_by = models.ForeignKey(ApplicationUser)
    tmp1 = models.CharField(max_length = 30, default="", blank=True, null=True)
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)

    @staticmethod
    def get_groups(page=0,span=GROUP_SPAN):
        result = Group.objects.order_by('-update_at').filter(isvalid__exact=True)
        if page!=0:
            page = page*GROUP_SPAN - GROUP_SPAN
        endpage = page + GROUP_SPAN
        return result[page:endpage],result.count()
    @staticmethod
    def group_list():
        return Group.objects.all()

    @staticmethod
    def get_by_name(name=""):
        result=None
        try:
            result = Group.objects.filter(name=name).get()
        except:
            result = None
        return result

    @staticmethod
    def get_by_id(keyid):
        result=None
        try:
            result = Group.objects.get(id__exact=keyid)
        except:
            result = None
        return result

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/isreport/group/%s" % self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)
    roman = models.CharField(max_length=255, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=True)
    create_by = models.ForeignKey(ApplicationUser)
    description = models.TextField(max_length = 1000, blank=True, null=True)
    tmp1 = models.TextField(max_length = 1000, blank=True, null=True)
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)
    def count_me(self):
        count = Entry.objects.filter(approval=True).filter(tag=self).filter(ispublic=True).count()
        return count
    def count_private_me(self):
        count = Entry.objects.filter(approval=True).filter(tag=self).count()
        return count
    def desc_me(self):
        if self.description:
            content = self.description
        else:
            content = (self.tmp1)
        # content = content.replace("\n","<br />")
        return content

    @staticmethod
    def get_tags(page=0,span=100):
        result = Tag.objects.order_by('-update_at').filter(isvalid__exact=True)
        if page!=0:
            page = page*span - span
        endpage = page + span
        return result[page:endpage],result.count()

    @staticmethod
    def get_by_id(keyid):
        result=None
        try:
            result = Tag.objects.get(id__exact=keyid)
        except:
            result = None
        return result


    @staticmethod
    def tag_list():
        return Tag.objects.order_by('-update_at').all()

    @staticmethod
    def get_by_name(name=""):
        result=None
        try:
            result = Tag.objects.filter(name=name).get()
        except:
            result = None
        return result

    def __unicode__(self):
        return self.name + u"（" +str(self.count_me())+u"）"

    def get_absolute_url(self):
        return "/isreport/tag/%s" % self.name

class Entry(models.Model):
    author = models.ManyToManyField(Author)
    path = models.CharField(max_length = 100)
    title = models.CharField(max_length = 255)
    abstract = models.TextField(max_length = 1000, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    # word = models.ManyToManyField(Word, blank=True, null=True)
    words = models.ManyToManyField('isnetwork.WordWrap', blank=True, null=True, db_index=True)
    # words = models.ManyToManyField(WordWrap, blank=True, null=True)
    group = models.ManyToManyField(Group, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, db_index=True)
    update_at = models.DateTimeField(auto_now=True, db_index=True)
    publish = models.DateTimeField(blank=True, null=True, db_index=True)
    upload_by = models.ForeignKey(ApplicationUser)
    isvalid = models.BooleanField(default=True)
    page = models.IntegerField(default=1)
    num = models.CharField(max_length = 20)
    # types = models.CharField(max_length = 20)
    section = models.TextField(max_length = 1000, blank=True, null=True)
    approval = models.BooleanField(default=False)
    isdraft = models.BooleanField(default=True)
    istext = models.BooleanField(default=True)
    ispdf = models.BooleanField(default=False)
    isapi = models.BooleanField(default=False)
    ispublic = models.BooleanField(default=True)
    public_level = models.IntegerField(default=0) #公開設定用 0で公開 1で完全非公開 2でタイトル、著者、アブストまで 3でタイトル、著者 4でタイトルのみ 5で文書の存在(Anonymouse)
    tmp1 = models.CharField(max_length = 30, default="", blank=True, null=True) #著者順用 ,区切りでauthor IDを入れる
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)
    # lang = models.IntegerField(max_length = 255,default=1) # 1ja 2en 3ch
    # extra_lang = models.ManyToManyField("self", blank=True, null=True)

    def get_favoritter(self):
        result = FavoriteHandler.get_by_entry(self)
        return result
    # def get_title(self):
    #     result = self.title
    #     reg = u"_//_"
    #     if result.count(reg) > 0:
    #         result = self.title.split(reg).get()
    #     return result
    #
    # def get_title_en(self):
    #     result = self.title
    #     reg = u"_//_"
    #     if result.count(reg) > 0:
    #         result = self.title.split(reg).get()
    #     return result
    @staticmethod
    def get_ranking(num=10, MEMCACHE=True):
        ranking = []
        memkey = "entry_ranking"+str(num)
        if MEMCACHE and memkey in cache:
            ranking = cache.get(memkey)
        else:
            sj_entries = []
            # try:
                # json = open('/Users/mmiyaji/Subversion/isreport/isbooks/isbookshelf/templates/isbookshelf/static/rank10.json',"r").read()
            try:
                json = open(STATIC_DIR+'isbookshelf/templates/isbookshelf/static/rank10.json',"r").read()
                sj = simplejson.loads(json)
                sj_entries = sj["entries"]
            except:
                pass
            count = 0
            for i in sj_entries:
                if count >= num:
                    break
                try:
                    entry = Entry.get_by_num(str(i["id"]))
                    ranking.append({"id":entry.id, "title":entry.title.replace('"','\"'), "count":i["ga:pageviews"]})
                    count += 1
                except:
                    pass
            if MEMCACHE and ranking:
                # cache生存時間 sec*min*hour
                calive = 60*60*8
                cache.set(memkey, ranking, calive)
                # ranking10.append(Entry.get_by_num(str(i["id"])))
        return ranking
    @staticmethod
    def get_rss(search_span):
        return Entry.objects.order_by('-publish').filter(isvalid=True).filter(approval=True).filter(isdraft=False).filter(ispublic=True)[0:search_span]

    @staticmethod
    def get_latest():
        try:
            return Entry.objects.order_by('-update_at').filter(isvalid=True).filter(approval=True).filter(isdraft=False).filter(ispublic=True).get()
        except:
            return None
    @staticmethod
    def get_approvals(page=0, issuper = False):
        result = Entry.objects.order_by('-publish').filter(isvalid=True).filter(approval__exact=False)
        if not issuper:
            result = result.filter(isdraft=False)
        if page!=0:
            page = page*10 - 10
        endpage = page + 10
        return result[page:endpage],result.count()

    @staticmethod
    def get_approvals_count():
        result = Entry.objects.filter(isvalid=True).filter(approval__exact=False).filter(isdraft=False)
        return result.count()

    @staticmethod
    def get_numbers(author):
        return Entry.objects.filter(author__exact=author).count()

    @staticmethod
    def isfirst(num):
        number = int(num)
        for i in xrange(10):
            if Entry.objects.filter(num__exact=str(number)).count()>0:
                number += 1
            else:
                break
        return str(number)

    @staticmethod
    def get_count(regist=False):
        result = Entry.objects.filter(approval=True).filter(isdraft=False)
        if not regist:
            result = result.filter(ispublic=True)
        return result.count()
    @staticmethod
    def get_by_id(keyid):
        result=None
        try:
            result = Entry.objects.get(id__exact=keyid)
        except:
            result = None
        return result

    @staticmethod
    def get_by_num(num):
        result=None
        try:
            result = Entry.objects.get(num__exact=num)
        except:
            result = None
        return result

    @staticmethod
    def get_my_reports(appuser,page=0):
        # result = Entry.objects.order_by('-update_at').filter(upload_by__exact=appuser)
        auth = Author.get_by_user(appuser)
        if not auth:
            return None,0
        result = Entry.objects.order_by('-update_at').filter(isvalid=True).filter(author__exact=auth)
        if page!=0:
            page = page*10 - 10
        endpage = page + 10
        return result[page:endpage],result.count()

    @staticmethod
    def get_item(target="",target_id="",author=None,year="",tag=None,keyword=None,
                    group=None,page=1,isdraft=False,regist=False,
                    stitle="",sauthor="",sabst="",stitles=None,sauthors=None,sabsts=None,
                    span=10,approval=True, isall=False,ignore=None):
        result = Entry.objects.order_by('-publish','-update_at').filter(isvalid=True)
        if approval:
            result = result.filter(approval=approval)
        # Author.objects.order_by('update_at').filter(rank="prof")
        valid = False
        if target_id:
            result = result.filter(id__exact=target_id)
            valid = True
        if tag:
            result = result.filter(tag__exact=tag)
            valid = True
        if keyword:
            result = result.filter(words__word__exact=keyword)
            valid = True
        if author:
            result = result.filter(author__exact=author)
            valid = True
        if group:
            result = result.filter(group__exact=group)
            valid = True
        if stitles:
            for i in stitles:
                if i:
                    result = result.filter(title__contains=i)
            valid = True
        if sauthors:
            for i in sauthors:
                if i:
                    auth = Author.get_by_s_name(i)
                    result = result.filter(author=auth)
            valid = True
        if sabsts:
            for i in sabsts:
                if i:
                    result = result.filter(abstract__contains=i)
            valid = True
        if stitle:
            result = result.filter(title__contains=stitle)
            valid = True
        if sauthor:
            auth = Author.get_by_s_name(sauthor)
            result = result.filter(author=auth)
            valid = True
        if sabst:
            result = result.filter(abstract__contains=sabst)
            valid = True
        if year:
            result = result.filter(publish__year=int(year))
            valid = True
        if ignore:
            result = result.exclude(id__exact=ignore.id)
            valid = True
        if isall:
            valid = True
        if not regist:
            result = result.filter(ispublic=True)
        # if tag:
        #     result = result.filter(tag__exact=tag)
        if valid:
            # 下書きをのぞく
            result = result.filter(isdraft=isdraft)
            if page!=0:
                page = page*span - span
            endpage = page + span
            if isall:
                result_entry = result
            else:
                result_entry = result[page:endpage]
            return result_entry,result.count()
        else:
            return None,0
    def show_escaped_title(self):
        title = self.title.strip().replace("'","\'").replace('"','\"').replace("  "," ")
        return title
    def show_create(self):
        date = self.create_at
        return date.strftime("%Y .%m .%d")

    def show_update(self):
        date = self.update_at
        return date.strftime("%Y .%m .%d %H:%M")

    def show_publish(self):
        date = self.publish
        return date.strftime("%Y-%m-%d")
        # return date.strftime("%Y .%m .%d")

    def show_pub_date(self):
        date = self.publish
        return date.strftime("%a, %d %b %Y %H:%M:%S +0900")

    def show_now_pub_date(self):
        date = datetime.datetime.now()
        return date.strftime("%a, %d %b %Y %H:%M:%S +0900")

    def get_publish(self):
        date = self.publish
        return date.strftime("%Y年%m月%d日")
    def get_publish_en(self):
        date = self.publish
        return date.strftime("%B %d. %Y")

    # ちょっと無謀な関連レポート計算。使わないよ
    def get_recommend_entry(self):
        t1 = time.time()
        # result = Entry.objects.order_by('-publish').filter(approval=True).filter(isdraft=False).filter(ispublic=True)
        result = self.words.all()
        if result:
            result = sorted(result,key=lambda x: x.tf*x.idf,reverse=True)#[:3]
        items = Entry.objects.order_by('-publish').filter(isvalid=True).filter(approval=True).filter(isdraft=False).filter(ispublic=True).exclude(id__exact=self.id)
        q = items
        old_q = q
        for c,w in enumerate(result):
            t2 = time.time() - t1
            if t2 > 10.0:
                q = None
                break
            # print c,#q,w
            q = q.filter(words__word__exact=w.word)
            if q.count() < 10:
                if q.count() < 3:
                    q = old_q
                    if c < 5:
                        continue
                    else:
                        break
                else:
                    break
            else:
                old_q = q
        # while self in q: q.remove(self)
        return q
        # queries = [models.Q(words__word__exact=w.word) for w in result]
        # query = queries.pop()
        # for q in queries:
        #     query |= q
        # items = items.filter(query)
        # output = []
        # for i in items:
        #     if not i in output:
        #         output.append(i)
        # return output

    # tfidf値でソートした単語列を返すよ
    def get_recommend_word(self, span=5, view_level=5):
        result = self.words.all().filter(isvalid=True).filter(word__view_level__gt=view_level)
        if result:
            result = sorted(result,key=lambda x: x.tf*x.idf,reverse=True)[:span]
        return result

    # 関連するレポートをparametaから計算するよ
    def calc_report(self, parameta=None, words = None, span=5, view_level=5):
        result = 0.0
        if parameta:
            for i in parameta:
                try:
                    ww = self.words.all().filter(isvalid=True).filter(word__exact=i.word).get()
                except:
                    ww = None
                if ww:
                    result += math.pow(ww.tf*ww.idf-i.score,2)
                else:
                    result += math.pow(i.score,2)
            result = math.sqrt(result)
            # print result
        elif words:
            for i in words:
                try:
                    ww = self.words.all().filter(isvalid=True).filter(word__exact=i.word).get()
                except:
                    ww = None
                if ww:
                    result += math.pow(ww.tf*ww.idf-i.tf*i.idf,2)
                else:
                    result += math.pow(i.tf*i.idf,2)
            result = math.sqrt(result)
            # print result
        else:
            print "not found"
        return result
    def authors(self):
        auths = self.author.all()
        # for au in auths:
        #     print au
        return auths

    def add_word(self,word):
        self.words.add(word)
        self.save()

    def add_authors_order(self,lists):
        self.tmp1 = lists
        self.save()

    def get_authors_order(self):
        if self.tmp1:
            auths = []
            auths_list = self.tmp1.split(",")
            for i in auths_list:
                if i:
                    auths.append(Author.get_by_id(int(i)))
        else:
            auths = self.author.all()
        return auths

    def groups(self):
        groups = self.group.all()
        return groups

    # モデルの命名ミスった wordに変えよう
    def wordss(self):
        wordss = self.words.all()
        return wordss

    def tags(self):
        tags = self.tag.all()
        return tags

    def sorted_tags(self):
        tags1 = self.tag.all()
        tags = []
        for i in tags1:
            tags.append(i)
        mins = 999
        mint = 0
        for c,i in enumerate(tags):
            tmp = ""
            mins = 999
            for j in xrange(c,len(tags)):
                if len(tags[j].name)<mins:
                    mins = len(tags[j].name)
                    mint = j
            tmp = tags[c]
            tags[c] = tags[mint]
            tags[mint] = tmp
        return tags

    def __unicode__(self):
        return self.title+u" :upload by "+self.upload_by.nickname + ", " + self.num

    def get_absolute_url(self):
        return "/isreport/entry/%i" % self.id

class BookHandler(models.Model):
    entries = models.ManyToManyField(Entry, blank=True, null=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    create_by = models.ForeignKey(ApplicationUser)
    book = models.ForeignKey(Book)
    isvalid = models.BooleanField(default=True)
    tmp1 = models.CharField(max_length = 30, default="", blank=True, null=True)
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)

    def get_entries(self):
        return self.entries.all()

    @staticmethod
    def get_by_book(book):
        if BookHandler.objects.filter(book=book).count()>0:
            return BookHandler.objects.filter(book=book).get()
        else:
            return None

    @staticmethod
    def get_by_appuser(appuser):
        if BookHandler.objects.filter(create_by=appuser).count()>0:
            return BookHandler.objects.filter(create_by=appuser).get()
        else:
            return None

    def __unicode__(self):
        return self.book.title

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id
    # class Meta:
    #     order_with_respect_to = 'question'

class FavoriteHandler(models.Model):
    entries = models.ManyToManyField(Entry, blank=True, null=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    create_by = models.ForeignKey(ApplicationUser)
    isvalid = models.BooleanField(default=True)
    tmp1 = models.CharField(max_length = 30, default="", blank=True, null=True)
    tmp2 = models.CharField(max_length = 30, default="", blank=True, null=True)

    def get_entries(self):
        return self.entries.all()

    @staticmethod
    def get_by_entry(entry):
        if FavoriteHandler.objects.filter(entries=entry).count()>0:
            return FavoriteHandler.objects.filter(entries=entry)
        else:
            return None

    @staticmethod
    def get_by_appuser(appuser):
        if FavoriteHandler.objects.filter(create_by=appuser).count()>0:
            return FavoriteHandler.objects.filter(create_by=appuser).get()
        else:
            return None

    def __unicode__(self):
        return self.create_by.nickname

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id
    # class Meta:
    #     order_with_respect_to = 'question'

class Meta:
    ordering = ['-create_at']
