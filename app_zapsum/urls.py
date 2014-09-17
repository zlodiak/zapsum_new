from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('app_zapsum',
    url(r'^$', 'views.rules', name='rules'),
    url(r'^search_author/$', 'views.search_author', name='search_author'),
    url(r'^search_record/$', 'views.search_record', name='search_record'),
    url(r'^last_records/$', 'views.last_records', name='last_records'),
    url(r'^most_popular_authors/$', 'views.most_popular_authors', name='most_popular_authors'),
    url(r'^new_authors/$', 'views.new_authors', name='new_authors'),
    url(r'^my_records/$', 'views.my_records', name='my_records'),
    url(r'^add_records/$', 'views.add_records', name='add_records'),
    url(r'^change_avatar/$', 'views.change_avatar', name='change_avatar'),
    url(r'^change_password/$', 'views.change_password', name='change_password'),
    url(r'^change_email/$', 'views.change_email', name='change_email'),
    url(r'^change_info/$', 'views.change_info', name='change_info'),
    url(r'^privacy_policy/$', 'views.privacy_policy', name='privacy_policy'),
    url(r'^change_profile/$', 'views.change_profile', name='change_profile'), 
    url(r'^change_profile_call/$', 'views.change_profile_call', name='change_profile_call'), 
)


