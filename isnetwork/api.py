#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by Masahiro MIYAJI on 2011-10-26.
Copyright (c) 2011 ISDL. All rights reserved.
"""

from isnetwork.models import *
from isbookshelf.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import *
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import time
import datetime
from utils import *
from getimageinfo import *
from isbookshelf.exceptions import Http403,Http404,Http500

def ajax(request,para):
	if para =="network":
		temp_values = Context()
		entry = None
		view_level = 5
		rank = 10
		layer = 1
		nodes = []
		if request.GET.has_key('id'):
			# entry = Entry.get_by_id(int(request.GET['id']))
			word = Word.get_by_id(int(request.GET['id']))
			if request.GET.has_key('layer'):
				layer = int(request.GET['layer'])
			if request.GET.has_key('view_level'):
				view_level = int(request.GET['view_level'])
		temp_values['nodes'] = get_network_node(word,times = layer, nodes = [],view_level=view_level)
		# temp_values['word'] = word
		# return render_to_response('isbookshelf/component/content_network_def.json',temp_values,
		return render_to_response('isbookshelf/component/content_network.json',temp_values,
					mimetype = "application/json",
					context_instance=RequestContext(request))
	elif para =="del_network":
		if request.user.is_authenticated():
			user = request.user
			appuser = ApplicationUser.get_by_user(user)
		if user.is_staff():
			temp_values = Context()
			view_level = 5
			layer = 1
			if request.POST.has_key('id'):
				word = Word.get_by_id(int(request.POST['id']))
				if request.POST.has_key('layer'):
					layer = int(request.POST['layer'])
				if request.POST.has_key('view_level'):
					view_level = int(request.POST['view_level'])
				word.view_level = view_level
				word.save()
				return HttpResponse("OK")
			else:
				return HttpResponse("NO")
		else:
			return HttpResponse("NO")

if __name__ == '__main__':
	main()

