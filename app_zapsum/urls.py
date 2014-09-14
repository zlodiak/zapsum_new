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
)


