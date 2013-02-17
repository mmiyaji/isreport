from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os


urlpatterns = patterns('',
                       # (r'^admin/(.*)', admin.site.root),
                       # url(r'^$', 'archives.general.home', name='home'),
                       (r'^isreport(/)?',include('isbookshelf.urls')),
                       # url(r'^(/)?', include('isbookshelf.urls')),
                       url(r'^404/$', 'isreport.views.status404', name='404'),
                       )

# if settings.DEBUG:
#     urlpatterns += patterns('',
#                             (r'^static/(?P<path>.*)$','django.views.static.serve',
#                              {'document_root': settings.MEDIA_ROOT}),
#                             (r'^media/(?P<path>.*)$','django.views.static.serve',
#                              {'document_root': settings.MEDIA_ROOT}),
#                             # (r'^admin/(?P<path>.*)$','django.views.static.serve',
#                             #  {'document_root': settings.ADMIN_MEDIA_PREFIX}),
#                             )
# # if settings.DEBUG:
# #     urlpatterns += patterns('',
# #             (r'^static/(?P<path>.*)$','django.views.static.serve',
# #                 {'document_root':os.path.dirname(__file__)+'/static'}),
# #             (r'^report/(?P<path>.*)$','django.views.static.serve',
# #                 {'document_root':os.path.dirname(__file__)+'isapps/report'}),
# #                 )
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            (r'^isapps/static/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            (r'^media/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
                            (r'^admin/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.ADMIN_MEDIA_PREFIX}),
                            )
