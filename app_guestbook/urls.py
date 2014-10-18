from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app_guestbook',
	url(r'^$', 'views.guestbook_tape', name='guestbook_tape'),
)
