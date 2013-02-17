#!/usr/bin/env python
# encoding: utf-8
"""
GAnalytics.py

Created by Masahiro MIYAJI on 2011-10-02.
Copyright (c)  ISDL. All rights reserved.
"""

import datetime, sys, os
import gdata.analytics.client
try:
	os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
	from models import *
except:
	pass
email="isgroupsystem@gmail.com"  # Set these values
password="hiroyasu.teikoku123"
table_ids = (
			'ga:36479471',		  # TABLE_ID for first website
			)

days = 30
span = 10
offset = 1
args = sys.argv
if len(args) > 1:
	days = int(args[1])
	span = int(args[2])
	offset = int(args[3])

SOURCE_APP_NAME = 'IS Report System client-v2'
client = gdata.analytics.client.AnalyticsClient(source=SOURCE_APP_NAME)
client.client_login(email, password, source=SOURCE_APP_NAME, service=client.auth_service)

today = datetime.date.today() - datetime.timedelta(days=offset)
lastmonth = today - datetime.timedelta(days=days)

for table_id in table_ids:   
	data_query = gdata.analytics.client.DataFeedQuery({
			'ids': table_id,
			'start-date': lastmonth.isoformat(),
			'end-date': today.isoformat(),
			'dimensions': 'ga:pagePath',
			'metrics': 'ga:pageviews,ga:uniquePageviews,ga:visits,ga:bounces',
			'sort': '-ga:pageviews',
			'filters': 'ga:pagePath=~(^/isreport/entry/.+|^/report/.+)',
			# 'filters': 'ga:pagePath=~^/report/.+',
			# 'filters': 'ga:pagePath=~^/isreport/entry/.+',
			'max-results': str(span),
			# 'metrics': 'ga:visitors'
			})
	feed = client.GetDataFeed(data_query)
	# if feed.entry:
	# 	print "%s : %s" % (feed.data_source[0].table_name.text, feed.entry[0].metric[0].value)
	# for count,entry in enumerate(feed.entry):
	# 	print count
	# 	for dim in entry.dimension:
	# 		print ('Dimension Name = %s \t Dimension Value = %s'
	# 			% (dim.name, dim.value))
	# 	for met in entry.metric:
	# 		print ('Metric Name    = %s \t Metric Value    = %s'
	# 			% (met.name, met.value))
	print '{ "entries":['
	for count,entry in enumerate(feed.entry):
		# print entry.title.text
		print '{"id":',
		for dim in entry.dimension:
			url = str(dim.value)
			entry_str = url.split("/")[-2]
			entry_id = 0
			isvalis = False
			try:
				entry_id = int(entry_str)
				isvalis = True
			except:
				pass
			if True:
				print '"'+entry_str+'"',
				for j in entry.metric:
					print ',"'+j.name+'":',j.value,
				print ',"url":"'+url+'"',
		print '}',
		if count < len(feed.entry)-1:
			print ','
	print '],'
	print '"start-date":"', lastmonth.isoformat(),'",'
	print '"end-date":"', today.isoformat(),'"',
	print '}'