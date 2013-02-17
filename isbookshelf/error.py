#!/usr/bin/env python
# encoding: utf-8
"""
error.py

Created by Masahiro MIYAJI on 2011-05-15.
Copyright (c) 2011 ISDL. All rights reserved.
"""

from views import *
from isbookshelf.exceptions import Http403,Http500
# from django.core.exceptions import PermissionDenied
def forbidden(request):
	# raise Http404
	temp_values = Context()
	temp_values['description'] = u"403 Forbidden Page."
	temp_values['navi']=get_navi("403Forbidden_/isreport/forbidden")
	temp_values['target']="forbidden"
	# request.status = 404
	raise Http403
	# raise PermissionDenied
	return render_to_response('403.html',temp_values,
					context_instance=RequestContext(request))

def notfound(request):
	temp_values = Context()
	temp_values['description'] = u"404 Not Found Page."
	temp_values['navi']=get_navi("404NotFound_/isreport/notfound")
	temp_values['target']="notfound"
	raise Http404
	return render_to_response('404.html',temp_values,
					context_instance=RequestContext(request))

def servererror(request):
	temp_values = Context()
	temp_values['description'] = u"500 Internal Server Error Page."
	temp_values['navi']=get_navi("500ServerError_/isreport/servererror")
	temp_values['target']="servererror"
	raise Http500
	return render_to_response('500.html',temp_values,
					context_instance=RequestContext(request))

def pagetemplate(request):
	temp_values = Context()
	return render_to_response('isbookshelf/oebps/page-template.xpgt',temp_values,
					context_instance=RequestContext(request))
