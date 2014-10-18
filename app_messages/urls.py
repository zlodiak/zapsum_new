from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('app_messages',
	url(r'^message_create/$', 'views.message_create', name='message_create', ),
	url(r'^message_sended_delete/$', 'views.message_sended_delete', name='message_sended_delete', ),
	url(r'^message_recieve_delete/$', 'views.message_recieve_delete', name='message_recieve_delete', ),
	#url(r'^message_sended/$', 'views.message_sended', name='message_sended', ),

	url(r'^messages_sended/$', 'views.messages_sended', name='messages_sended', ),
	url(r'^messages_sended/(?P<message_id>[0-9]*)/$', 'views.messages_sended_item', name='messages_sended_item', ),

	url(r'^messages_recieve/$', 'views.messages_recieve', name='messages_recieve', ),
	url(r'^messages_recieve/(?P<message_id>[0-9]*)/$', 'views.messages_recieve_item', name='messages_recieve_item', ),
)


