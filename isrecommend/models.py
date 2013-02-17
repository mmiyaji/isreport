# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth_models
# from django.utils import simplejson
from isbookshelf.models import *
from isnetwork.models import *
from isrecommend.models import *
# from ishistory.models import *
import datetime,time
# from django.db.models import Q

class Parameta(models.Model):
    appuser = models.ForeignKey(ApplicationUser, db_index=True)
    word = models.ForeignKey(Word, db_index=True)
    score = models.FloatField(default=0.0, blank=True, null=True, db_index=True)
    rank = models.IntegerField(default=0, blank=True, null=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=True)

    @staticmethod
    def get_param(user):
        try:
            result = Parameta.objects.filter(appuser=user).order_by('-rank')
        except:
            result = None
        return result

    def __unicode__(self):
        return self.appuser.nickname +" : "+self.word.name+" : score( "+str(self.score)+" ), "+str(self.create_at)

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id

class Individual(models.Model):
    """
    GAにおける遺伝子表現
    """
    appuser = models.ForeignKey(ApplicationUser, db_index=True)
    parameta = models.ManyToManyField(Parameta, blank=True, null=True)
    gene_index = models.IntegerField(default=0, blank=True, null=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=True)

    @staticmethod
    def delete_individual(appuser):
        try:
            Individual.objects.filter(appuser=appuser).delete()
        except:
            pass

    @staticmethod
    def get_individual(appuser):
        try:
            result = Individual.objects.filter(appuser=appuser).order_by('-gene_index')
        except:
            result = None
        return result

    def get_params(self):
        try:
            result = self.parameta.all().order_by('-score')
        except:
            result = None
        return result

    def __unicode__(self):
        p = ""
        for i in self.get_params():
            p += " "+i.word.name+"("+str(i.word.id)+"),"
        return self.appuser.nickname +" : gene_index( "+str(self.gene_index)+" ), " +p+str(self.update_at)

    def get_absolute_url(self):
        return "/isbookshelf/detail/%i" % self.id
class Meta:
    ordering = ['-create_at']
