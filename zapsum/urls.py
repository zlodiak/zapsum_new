from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app_zapsum.views.rules', name='rules'),
    url(r'^search_author$', 'app_zapsum.views.search_author', name='search_author'),

    url(r'^admin/', include(admin.site.urls)),
)
