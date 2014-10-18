from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('app_zapsum.urls')),
	url(r'^accounts/', include('app_accounts.urls')),
	url(r'^messages/', include('app_messages.urls')),
	url(r'^summernote/', include('django_summernote.urls')),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^admin/', include(admin.site.urls)),	
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )


urlpatterns += patterns('app_zapsum',	
	url(r'^.*/', 'views.page_error404', ),
)    

