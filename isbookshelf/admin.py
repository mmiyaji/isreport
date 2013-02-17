#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by mmiyaji on 2013-02-17.
Copyright (c) 2013  ruhenheim.org. All rights reserved.
"""
from isbookshelf.models import *
from isrecommend.models import *
from ishistory.models import *
from isnetwork.models import *
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    pass

# モデルをadminサイトに表示させる
admin.site.register(ApplicationUser, AuthorAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Word, AuthorAdmin)
admin.site.register(WordWrap, AuthorAdmin)
admin.site.register(Entry, AuthorAdmin)
admin.site.register(Tag, AuthorAdmin)
admin.site.register(Group, AuthorAdmin)
admin.site.register(Book, AuthorAdmin)
admin.site.register(BookHandler, AuthorAdmin)
admin.site.register(Favorite, AuthorAdmin)
admin.site.register(FavoriteHandler, AuthorAdmin)
admin.site.register(UserEntryHistory, AuthorAdmin)
admin.site.register(Parameta, AuthorAdmin)
admin.site.register(Individual, AuthorAdmin)
