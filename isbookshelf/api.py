#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by Masahiro MIYAJI on 2011-10-26.
Copyright (c) 2011 ISDL. All rights reserved.
"""
from views import *
from django.contrib.auth.decorators import login_required
def get_network_node(word, times=0, nodes = [],view_level=4):
	master_node = Edge.get_by_word(word,view_level=view_level)
	master_node = sorted(master_node,key=lambda x: x.count,reverse=True)[0:10]
	# nodes.append(master_node)
	edges = []
	for i in master_node:
		wo = None
		if i.word1 == word:
			wo = i.word2
		else:
			wo = i.word1
		if times>0:
			local_edges = get_network_node(wo, times = times-1, nodes = nodes,view_level=view_level)
			m_node = {"id":wo.id, "name":wo.name+"["+str(wo.count_me())+"]", "edges":local_edges}
			nodes.append(local_edges)
		else:
			m_node = {"id":wo.id, "name":wo.name+"["+str(wo.count_me())+"]"}
		edges.append(m_node)
	node = {"id":word.id, "name":word.name+"["+str(word.count_me())+"]", "edges":edges}
	nodes.append(node)
	# print nodes
	return nodes

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
		if user.is_staff:
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

