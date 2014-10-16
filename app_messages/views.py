from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.contrib import auth
from django import forms
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app_messages.models import Message
from app_messages.forms import MessageForm


def custom_proc(request):
	"""
	request object for every pages
	"""		
	return{
		'request': request,
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
	if request.method == 'POST':		
		delete_id = request.POST.get('delete_id', '')	
		try:
			Message.delete_message(delete_id)		
		except:
			return HttpResponseRedirect('/page_error404/')
			
		
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
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	
	

@login_required	
def messages_sended(request):	
	if request.method == 'POST':		
		delete_id = request.POST.get('delete_id', '')	
		try:
			Message.delete_message(delete_id)		
		except:
			return HttpResponseRedirect('/page_error404/')
				
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
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	

	

@login_required	
def message_create(request, id_reciever=None):	
	form = MessageForm()

	if request.method == 'POST':	
		pass
		
	# obj_reciever = None
	
	# if id_reciever:
	# 	obj_reciever = UserProfile.get_entry(user_id=int(id_reciever))
		
	# if request.method == 'POST':											
	# 	form = MessageForm(request.POST)
	# 	if form.is_valid():		
	# 		theme = form.cleaned_data.get('theme') or None
	# 		text = form.cleaned_data.get('text') or None
								
	# 		Message(
	# 			sender=request.user,
	# 			reciever=obj_reciever,
	# 			theme=theme,
	# 			text=text,
	# 		).save()
	# 		return HttpResponseRedirect('/userprofile/message_sended/')						
        		
	t = loader.get_template('message_create.html')
	c = RequestContext(request, {
		'form': form,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	
	
	
def message_sended(request):
	t = loader.get_template('message_sended.html')
	c = RequestContext(request, {}, [custom_proc])	
	return HttpResponse(t.render(c))