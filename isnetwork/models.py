# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import simplejson
from isbookshelf.models import *
from isnetwork.models import *
import datetime,time
from django.db.models import Q

class Word(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    roman = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    yomi = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    view_level = models.IntegerField(default=100, blank=True, null=True, db_index=True)#初期値100で1から順に足切りレベル上げる
    title_count = models.IntegerField(default=0, blank=True, null=True)
    abst_count = models.IntegerField(default=0, blank=True, null=True)
    content_count = models.IntegerField(default=0, blank=True, null=True)
    other_count = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField(max_length = 2000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=True)

    def count_me(self):
        # count = Entry.objects.filter(approval=True).filter(words__word__exact=self).filter(ispublic=True).count()
        # return count
        return self.other_count

    def count_private_me(self):
        # count = Entry.objects.filter(approval=True).filter(words__word__exact=self).count()
        # return count
        return self.other_count

    def desc_me(self):
        content = (self.description)
        # content = content.replace("\n","<br />")
        return content

    def get_nodes(self, view_level = 4, rank=10):
        nodes = []
        e1 = Edge.get_by_word(self, view_level=view_level)
        result = sorted(e1,key=lambda x: x.count,reverse=True)[0:rank]
        for i in result:
            if i.word1 == self:
                nodes.append(i.word2)
            else:
                nodes.append(i.word1)
        return nodes

    @staticmethod
    def add_word(name,reference="",roman="",description="",
            view_level=0, title_count=0, abst_count=0, content_count=0, other_count=0, isvalid=True):
        result = None
        if name:
            result = Word.get_by_name(name)
            if not result:
                result = Word(name=name,roman=roman,description=description)
                result.save()
            if reference == "title":
                result.title_count +=1
            elif reference == "abst":
                result.abst_count +=1
            elif reference == "content":
                result.content_count +=1
            elif reference == "other":
                result.other_count +=1
            else:
                other_count +=1

            result.view_level = view_level
            result.title_count = title_count
            result.abst_count = abst_count
            result.content_count = content_count
            result.other_count = other_count
            result.isvalid = isvalid

            result.save()
        return result

    @staticmethod
    def get_words(page=0,span=100,view_level=5):
        # result = Word.objects.order_by('-update_at').filter(isvalid__exact=True)
        result = Word.objects.order_by('-other_count').filter(isvalid__exact=True)
        if view_level:
            result = result.filter(view_level__gt=view_level)
        if page!=0:
            page = page*span - span
        endpage = page + span
        return result[page:endpage],result.count()

    @staticmethod
    def get_by_id(keyid):
        result=None
        try:
            result = Word.objects.get(id__exact=keyid)
        except:
            result = None
        return result

    @staticmethod
    def word_list():
        return Word.objects.order_by('-update_at').all()

    @staticmethod
    def get_by_name(name=""):
        result=None
        try:
            result = Word.objects.order_by('name').filter(name=name)[0]
        except:
            result = None
        return result

    @staticmethod
    def get_item(target="",target_id="",year="",
                    span=10,page=1,regist=False,
                    sname="",sroman="",snames=None,sromans=None,
                    isvalid=False,view_level=0,rev=False
                    ):
        # result = Word.objects.order_by('-update_at')
        # result = Word.objects.order_by('-name')
        if rev:
            result = Word.objects.order_by('-other_count')
        else:
            result = Word.objects.order_by('other_count')

        valid = True
        if isvalid:
            result = result.filter(isvalid=isvalid)
            valid = True
        if view_level:
            result = result.filter(view_level__gt=view_level)
            valid = True
        if target_id:
            result = result.filter(id__exact=target_id)
            valid = True
        if snames:
            for i in snames:
                if i:
                    result = result.filter(name__contains=i)
            valid = True
        if sromans:
            for i in sromans:
                if i:
                    result = result.filter(roman__contains=i)
            valid = True
        if sname:
            result = result.filter(name__contains=sname)
            valid = True
        if sroman:
            result = result.filter(roman__contains=sroman)
            valid = True
        if year:
            result = result.filter(update_at__year=int(year))
            valid = True
        if valid:
            if span==0:
                return result.all(),result.count()
            else:
                if page!=0:
                    page = page*span - span
                endpage = page + span
                return result[page:endpage],result.count()
        else:
            return None,0
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id


class WordWrap(models.Model):
    word = models.ForeignKey(Word, db_index=True)
    count = models.IntegerField(default=0, blank=True, null=True, db_index=True)
    tf = models.FloatField(default=0.0, blank=True, null=True, db_index=True)
    idf = models.FloatField(default=0.0, blank=True, null=True, db_index=True)
    score = models.FloatField(default=0.0, blank=True, null=True, db_index=True)
    # reference = models.CharField(default="title", blank=True, null=True)
    description = models.TextField(max_length = 2000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=True)

    def tfidf(self):
        return self.tf*self.idf
    def __unicode__(self):
        return self.word.name +": tf="+str(self.tf)+", idf="+str(self.idf)

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id

class Edge(models.Model):
    word1 = models.ForeignKey(Word,related_name='word1', db_index=True)
    word2 = models.ForeignKey(Word,related_name='word2', db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=True)
    score = models.FloatField(default=0.0, blank=True, null=True, db_index=True)
    count = models.IntegerField(default=0, blank=True, null=True, db_index=True)
    description = models.TextField(max_length = 2000, blank=True, null=True)

    # def get_nodes(self):
    #
    #     return result

    @staticmethod
    def add_edge(word1=None,word2=None,edge_count=1,score=0.0):
        e = Edge.get_by_words(word1,word2)
        if not e:
            e = Edge()
            e.word1 = word1
            e.word2 = word2
            e.score = score
        e.count += edge_count
        e.save()
        return e

    @staticmethod
    def get_by_words(word1=None,word2=None,view_level=4):
        result = None
        if word1 and word2:
            try:
                result = Edge.objects.filter(word1=word1).filter(word2=word2)[0]
            except:
                pass
            if not result:
                try:
                    result = Edge.objects.filter(word1=word2).filter(word2=word1)[0]
                except:
                    pass
        return result

    @staticmethod
    def get_by_word(word=None, view_level=4 ,span = 0):
        result = None
        if word:
            query = Q(word1__exact=word)|Q(word2__exact=word)
            result = Edge.objects.filter(word1__view_level__gt=view_level).filter(word2__view_level__gt=view_level).filter(query)
            if span:
                result = sorted(result,key=lambda x: x.count,reverse=True)[0:span]
        return result

    def __unicode__(self):
        return self.word1.name+"("+ str(self.word1.id) +"):"+self.word2.name +"("+ str(self.word2.id) +") ["+str(self.count) +":"+ str(self.score)+"]"

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id

class Meta:
    ordering = ['-create_at']
