from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.contrib import auth
from django import forms
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app_messages.models import Modal, Message
from app_accounts.models import UserProfile
from app_messages.forms import MessageForm, CreateMessageForm


def custom_proc(request):
	"""
	request object for every pages
	also transmitted messages for modal windows
	"""		
	modal = Modal.get_entries()
	return{
		'request': request,
		'modal': modal,
	}


@login_required	
def messages_sended_item(request, message_id):	
	message_obj = Message.get_message(message_id=message_id)
        		
	t = loader.get_template('messages_sended_item.html')
	c = RequestContext(request, {
		'message_obj': message_obj,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	
	
	
@login_required	
def messages_recieve_item(request, message_id):	
	message_obj = Message.get_message(message_id=message_id)
        		
	t = loader.get_template('messages_recieve_item.html')
	c = RequestContext(request, {
		'message_obj': message_obj,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	
	
	
@login_required	
def messages_recieve(request):	
	action = None
	if request.GET.get('action'):
		action = int(request.GET.get('action'))	

	exists_recieve_messages = Message.exists_recieve_messages(request.user.id)
	messages_recieve = Message.get_recieve_messages(request.user.id)
	paginator = Paginator(messages_recieve, 10)
	list_pages = paginator.page_range
	
	page = request.GET.get('page')
	try:
		messages_recieve_paginated = paginator.page(page)
	except PageNotAnInteger:
		messages_recieve_paginated = paginator.page(1)
	except EmptyPage:
		messages_recieve_paginated = paginator.page(paginator.num_pages)	
		
	last_page = list_pages[-1]	
	first_page = list_pages[0]		
        		
	t = loader.get_template('messages_recieved.html')
	c = RequestContext(request, {
		'exists_recieve_messages': exists_recieve_messages,
		'list_pages': list_pages,
		'messages_recieve_paginated': messages_recieve_paginated,
		'last_page': last_page,
		'first_page': first_page,	
		'action': action,		
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	
	

@login_required	
def messages_sended(request):
	action = None
	if request.GET.get('action'):
		action = int(request.GET.get('action'))	
				
	exists_sended_messages = Message.exists_sended_messages(request.user.id)
	messages_sended = Message.get_sended_messages(request.user.id)
	paginator = Paginator(messages_sended, 10)
	list_pages = paginator.page_range
	
	page = request.GET.get('page')
	try:
		messages_sended_paginated = paginator.page(page)
	except PageNotAnInteger:
		messages_sended_paginated = paginator.page(1)
	except EmptyPage:
		messages_sended_paginated = paginator.page(paginator.num_pages)	
		
	last_page = list_pages[-1]	
	first_page = list_pages[0]			
        		
	t = loader.get_template('messages_sended.html')
	c = RequestContext(request, {
		'exists_sended_messages': exists_sended_messages,
		'list_pages': list_pages,
		'messages_sended_paginated': messages_sended_paginated,
		'last_page': last_page,
		'first_page': first_page,		
		'action': action,		
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	

	

@login_required	
def message_create(request, id_reciever=None):	
	form = CreateMessageForm()	
		
	if request.method == 'POST':											
		form = CreateMessageForm(request.POST)
		if form.is_valid():		
			reciever = form.cleaned_data.get('reciever') or None	
			theme = form.cleaned_data.get('theme') or None 			
			text = form.cleaned_data.get('text') or None 			
								
			Message(
				sender=request.user,	
				reciever=reciever,		
				theme=theme,			
				text=text,				
			).save()
			return HttpResponseRedirect('/messages/messages_sended/?action=0')						
        		
	t = loader.get_template('message_create.html')
	c = RequestContext(request, {
		'form': form,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	
	

def message_sended_delete(request):
	if request.method == 'POST':		
		delete_id = request.POST.get('delete_id', '')	
		Message.delete_sended_message(delete_id)		

	return HttpResponseRedirect('/messages/messages_sended/?action=1')


def message_recieve_delete(request):
	if request.method == 'POST':		
		delete_id = request.POST.get('delete_id', '')	
		Message.delete_recieved_message(delete_id)		

	return HttpResponseRedirect('/messages/messages_recieve/?action=1')	
