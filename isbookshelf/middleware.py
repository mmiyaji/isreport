#!/usr/bin/env python
# encoding: utf-8
"""
middleware.py

Created by Masahiro MIYAJI on 2011-05-17.
Copyright (c) 2011 ISDL. All rights reserved.
"""
from django.http import HttpResponseForbidden
from django.template import Context
from django.template.loader import get_template
from isbookshelf.exceptions import Http403,Http404,Http500
from settings import *
class ExceptionMiddleware(object):
	def _get_forbidden(self):
		t = get_template("403.html")
		context = Context()
		context["MEDIA_URL"] = MEDIA_URL
		return HttpResponseForbidden(t.render(context))
	def _get_notfound(self):
		t = get_template("404.html")
		context = Context()
		context["MEDIA_URL"] = MEDIA_URL
		context["description"] = "404 Not Found Page. お探しのページが見つかりません．"
		return HttpResponseForbidden(t.render(context))
	def _get_internal(self):
		t = get_template("500.html")
		context = Context()
		context["MEDIA_URL"] = MEDIA_URL
		return HttpResponseForbidden(t.render(context))

	def process_exception(self, request, e):
		if isinstance(e, Http403):
			return self._get_forbidden()
		elif isinstance(e, Http404):
			return self._get_notfound()
		elif isinstance(e, Http500):
			return self._get_internal()
		else:
			return None
