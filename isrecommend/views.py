# -*- coding: utf-8 -*-
import os,re
import commands
from isreport.settings import *
from ishistory.models import *
from isnetwork.models import *
from isrecommend.models import *
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
import datetime,random
from utils import *
from getimageinfo import *
import isbooks.networkx as nx
from django.core.cache import cache

try:
	from isbooks.isbookshelf.exceptions import Http403,Http404,Http500
except:
	pass
DEBUG = False

def calc_recom(request=None, new_entry=Entry.get_by_id(1100), old_entry=Entry.get_by_id(110), user = None, appuser = None):
	result = None
	if not appuser:
		if request.user.is_authenticated():
			user = request.user
			appuser = ApplicationUser.get_by_user(user)
	result,ostatuses,nstatuses,xstatuses = find_recom(user, appuser, new_entry)
	return result
def wizard(e1 = 1, e2 = 2):
	new_entry=Entry.get_by_id(e1)
	old_entry=Entry.get_by_id(e2)
	fruit(new_entry, old_entry)
	
def mistic(s = 0, e = 1):
	for i in range(s,e):
		new_entry=Entry.get_by_id(i)
		if new_entry:
			for j in range(1,1565):
				old_entry=Entry.get_by_id(j)
				if old_entry:
					fruit(new_entry, old_entry)
	print "OWARI"
	
def fruit(new_entry=Entry.get_by_id(1100), old_entry=Entry.get_by_id(110),appuser = ApplicationUser.get_by_name("mmiyaji")):
	Individual.delete_individual(appuser)
	result,ostatuses,nstatuses,xstatuses,natural_result = find_recom(user = True, appuser = appuser, new_entry = new_entry, old_entry = old_entry)
	t_content = loader.get_template('isbookshelf/component/export_log.csv')
	c_content = Context()
	c_content['nentry'] = new_entry
	c_content['oentry'] = old_entry
	c_content['naentry'] = natural_result
	c_content['reentry'] = result
	c_content['nstatuses'] = nstatuses
	c_content['ostatuses'] = ostatuses
	c_content['xstatuses'] = xstatuses
	r_text = HttpResponse(t_content.render(c_content)).content
	flog = open("isbookshelf/recom_log/"+str(new_entry.id)+"_"+str(old_entry.id)+".log","w")
	flog.write(HttpResponse(t_content.render(c_content)).content)
	flog.close()
	return result
def natural_recom(new_entry):
	result = None
	entry_span = 10 #population size
	word_span = 10 #gene length
	mem_entry = "entry"+str(new_entry.id)+"_wspan"+str(word_span)+"_espan"+str(entry_span)

	if mem_entry in cache:
		print "already calced entry recom",mem_entry
		result = cache.get(mem_entry)
	else:
		print "create new entry recom",mem_entry
		words = new_entry.get_recommend_word(span=word_span)
		# entry,count = Entry.get_item(isall=True)
		entry,count = Entry.get_item(isall=True,ignore = new_entry)
		result = sorted(entry,key=lambda x: x.calc_report(words=words),reverse=False)[:entry_span]
		cache.set(mem_entry,result,0)
	return result
	
def find_recom(user = True, appuser = None, new_entry = None, old_entry = None, RECOMMEND=RECOMMEND):
	result = None
	EXP = True
	entry_span = 10 #population size
	word_span = 10 #gene length
	yarinaoshi = True
	ostatuses = []
	nstatuses = []
	xstatuses = []
	
	natural_result = natural_recom(new_entry)
	if not user or not appuser or not RECOMMEND:
		yarinaoshi = False
		result = natural_recom(new_entry)
		# result = random.sample(entry,entry_span)
	else:
		length = None
		path = None
		result = []
		words = new_entry.get_recommend_word(span=word_span) 
		# params = Parameta.get_param(appuser) 
		
		# start実験
		individuals = []
		if EXP:
			owords = old_entry.get_recommend_word(span=word_span)
			sum_score = 0.0
			for j in owords:
				sum_score += j.tf * j.idf
			for i in range(0,entry_span):
				individual = Individual()
				individual.appuser = appuser
				individual.save()
				for pc,w in enumerate(owords):
					p = Parameta()
					p.appuser = appuser
					p.word = w.word
					p.score = w.tf * w.idf / sum_score 
					p.save()
					# ostatuses.append({"word":p.word,"score":p.score,"in_id":i,"p_id":pc})
					# ostatuses.append({"word":p.word,"score":p.score,"in_id":i,"p_id":pc})
					individual.parameta.add(p)
				individual.save()
				individuals.append(individual)
		else:
			individuals = Individual.get_individual(appuser) 
		# end実験

		sum_score = 0.0
		for j in words:
			sum_score += j.tf * j.idf
		for j in words:
			nstatuses.append({"word":j.word,"score":(j.tf*j.idf)/sum_score})
		
		if individuals:
			G = get_network("network_lim3")
			for inc,individual in enumerate(individuals):
				params = individual.get_params()
				# params = sorted(params,key=lambda x: x.score,reverse=True)
				new_param_node = []
				new_param_score = []
				xpaths = []
				new_param_max = 0
				pc = 0
				for p,w in zip(params, words):
					length = None
					path = None
					ostatuses.append({"word":p.word,"score":p.score,"in_id":inc,"p_id":pc})
					pc += 1
					if cache.has_key("netpath_"+str(w.word.id)):
						length,path=cache.get("netpath_"+str(w.word.id))
						print "not",w.word.id
					else:
						length,path=nx.single_source_dijkstra(G,w.word.id)
						cache.set("netpath_"+str(w.word.id),[length,path],0)
						print "find",w.word.id
					paths = path[p.word.id]
					if paths:
						index = 1.0
						rand_max = 0
						rand_span = 0
						# score = w.tf * w.idf
						score = (w.tf*w.idf)/sum_score
						rand_max = score
						if score > p.score:
							index = -1.0
						rand_span = ((p.score - score)*index)/len(paths)
						randvalue_nodes = [score]
						path_nodes = [w.word]
						print rand_max,
						for i in xrange(1,len(paths)-1):
							path_nodes.append(Word.get_by_id(paths[i]))
							plus = rand_span*index*i + score
							rand_max += plus
							randvalue_nodes.append(plus)
							print plus,
						rand_max += p.score
						randvalue_nodes.append(p.score)
						print p.score
						path_nodes.append(p.word)
						print "max:",rand_max
						print path_nodes,score,":",p.score,"#",randvalue_nodes
						rand = random.random()*rand_max
						roulette_index = 0
						roulette_value = 0
						for j in range(0,len(randvalue_nodes)):
							roulette_value += randvalue_nodes[j]
							if roulette_value > rand:
								roulette_index = j
								break
						print "rand",rand,roulette_index,path_nodes[roulette_index]
						print randvalue_nodes[roulette_index]
						new_param_max += randvalue_nodes[roulette_index]
						print path_nodes[roulette_index]
						new_param_node.append(path_nodes[roulette_index])
						new_param_score.append(randvalue_nodes[roulette_index])

						xpaths.append({"paths":path_nodes, "vals":randvalue_nodes})
				for c,p in enumerate(params):
					# print params,new_param_node,c,words
					if new_param_node[c]:
						p.word = new_param_node[c]
						p.score = new_param_score[c]/new_param_max
						p.save()
						xstatuses.append({"word":p.word,"score":p.score,"in_id":inc,"p_id":c,"xpaths":xpaths})
					else:
						break
		else:
			print "no param"
			individuals = []
			for i in range(0,entry_span):
				individual = Individual()
				individual.appuser = appuser
				individual.save()
				for pc,w in enumerate(words):
					p = Parameta()
					p.appuser = appuser
					p.word = w.word
					p.score = w.tf * w.idf / sum_score 
					p.save()
					# ostatuses.append({"word":p.word,"score":p.score,"in_id":i,"p_id":pc})
					xstatuses.append({"word":p.word,"score":p.score,"in_id":i,"p_id":pc})
					individual.parameta.add(p)
				individual.save()
				individuals.append(individual)
			print "set param"
		# params = Parameta.get_param(appuser)
		# print params
		entry,count = Entry.get_item(isall=True,ignore = new_entry)
		if yarinaoshi:
			for c,i in enumerate(individuals):
				print c
				params = i.get_params()
				print params
				ign_num = []
				calc_entry = []
				for y in entry:
					calc_entry.append(y.calc_report(parameta=params))
				for j in range(0,entry_span):
					max_index = 0
					max_val = 999999 #距離の最小化問題なので本当はmin
					for index,x in enumerate(entry):
						if index not in ign_num:
							# x_val = x.calc_report(params)
							x_val = calc_entry[index]
							if max_val > x_val:
								max_val = x_val
								max_index = index
					if entry[max_index] not in result:
						result.append(entry[max_index])
						print entry[max_index],max_index,max_val
						break
					else:
						print "yarinaosi",entry[max_index],max_index,max_val
						ign_num.append(max_index)
		else:
			print "gakushu nashi"
			result = sorted(entry,key=lambda x: x.calc_report(params),reverse=False)[0:entry_span]
					# entry.pop(max_index)
			# sorted_entry = sorted(entry,key=lambda x: x.calc_report(params),reverse=False)
			# for i in sorted_entry:
			# 	if i not in result:
			# 		result.append(i)
			# 		break
		# result = random.sample(entry,entry_span)
		# for i in range(0,entry_span):
		# 	print i
		# result[0].calc_report(params)
		# result = sorted(entry,key=lambda x: x.calc_report(params),reverse=False)[0:entry_span]
		print result,
	return result,ostatuses,nstatuses,xstatuses,natural_result
def get_top_repo(self, G, param, entry, span=1):
	"""docstring for get_top_repo"""
	pass
def get_network(memkey="network_lim3"):
	G = None
	if MEMCACHE and not cache.has_key(memkey):
	# if True:
		G = recalc_network()
	else:
		G = cache.get(memkey)
	return G

def calc_param():
	G = None
	if MEMCACHE and not cache.has_key('network_lim3'):
	# if True:
		G = recalc_network()
	cached = None
	try:
		length,path=nx.single_source_dijkstra(G,1129)
		cached = path
	except:
		pass
	# print cached,cache

def recalc_network(memkey="network_lim3", memtime=0, netlim=3, edge_max=671.0, span = 20000):
	G=nx.Graph()
	words,count = Word.get_words(span=span)
	max = 0
	min = 999999
	for c,word in enumerate(words):
		print c+1,"/",count
		master_node = Edge.get_by_word(word,view_level=5)
		nodes = sorted(master_node,key=lambda x: x.count,reverse=True)[0:netlim]
		for j in nodes:
			cc = j.count
			G.add_node(j.word1.id)
			G.add_node(j.word2.id)
			wei = 1.0-cc/edge_max
			if wei < 0:
				wei = 0
			G.add_edge(j.word1.id,j.word2.id, weight=wei)
			if max < cc:
				max = cc 
			if min > cc:
				min = cc
	cache.set(memkey, G, memtime)
	return cache.get(memkey)

