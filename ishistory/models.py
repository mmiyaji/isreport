# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth_models
# from django.utils import simplejson
from isbookshelf.models import *
from isnetwork.models import *
from ishistory.models import *
import datetime,time
# from django.db.models import Q

class UserEntryHistory(models.Model):
    appuser = models.ForeignKey(ApplicationUser, blank=True, null=True, db_index=True)
    entry = models.ForeignKey(Entry, db_index=True)
    sessionid = models.CharField(max_length = 40, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    isvalid = models.BooleanField(default=True)

    @staticmethod
    def save_history(entry, session, user = None):
        history = UserEntryHistory()
        history.appuser = user
        history.sessionid = session
        history.entry = entry
        history.save()
        return history

    def __unicode__(self):
        name = "Anonymous"
        if self.appuser:
            name = self.appuser.nickname
        return name +" : "+self.entry.title+", "+str(self.create_at) + ", sessionID( "+ self.sessionid +" )"

    def get_absolute_url(self):
        return "/isreport/entry/%i" % self.entry.id

class Meta:
    ordering = ['-create_at']
