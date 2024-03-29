﻿# -*- coding:utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sorl.thumbnail import delete
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from app_accounts.forms import ProfileForm
from app_accounts.models import UserProfile, Gender
from app_zapsum.models import Diary
from app_zapsum.forms import ChangePasswordForm, ChangeAvatarForm, addMessageForm
from app_messages.models import Modal

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


def rules(request):	
	"""
	template for rules page
	"""	
	t = loader.get_template('page_rules.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def search_author(request):	
	"""
	data for render search author page
	"""
	if request.method == "POST":
		result = False
		author = request.POST.get('author', '')	
		authors_list = UserProfile.get_authors_list(author=author)
		authors_list_obj = [{k: v for k, v in authors_list}]

		if len(authors_list) > 0:
			authors_list_obj = [{k: v for k, v in authors_list}]
		else:
			authors_list_obj = None

		return HttpResponse(json.dumps(authors_list_obj), content_type='application/json')		

	t = loader.get_template('page_search_author.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	

def record(request, id_record):	
	"""
	data for render record public page
	"""	
	entry = Diary.get_entry_public(id_record=id_record)
	print(entry.date)
	print(entry.last_edit_date)

	user_entry = UserProfile.get_entry(user_id=entry.user_id)
	user_entry.views = user_entry.views + 1
	user_entry.save()

	avatar = user_entry.avatar		

	t = loader.get_template('page_record.html')
	c = RequestContext(request, {
		'entry': entry,
		'avatar': avatar,
		'nickname': user_entry.nickname,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 		


def diary(request, id_author=None):	
	"""
	data for render public records on diary page
	"""	
	if id_author:
		obj_author = UserProfile.get_entry(user_id=id_author)
		obj_diary = Diary.get_all_user_entries(user_id=id_author)

		user_entry = UserProfile.get_entry(user_id=id_author)
		user_entry.views = user_entry.views + 1
		user_entry.save()		

		paginator = Paginator(obj_diary, 6)
		list_pages = paginator.page_range

		page = request.GET.get('page')
		try:
			obj_diary_paginated = paginator.page(page)
		except PageNotAnInteger:
			obj_diary_paginated = paginator.page(1)
		except EmptyPage:
			obj_diary_paginated = paginator.page(paginator.num_pages)	

		last_page = list_pages[-1]	
		first_page = list_pages[0]			

		t = loader.get_template('page_diary.html')
		c = RequestContext(request, {
			'obj_author': obj_author,
			'obj_diary': obj_diary,
			'list_pages': list_pages,
			'obj_diary_paginated': obj_diary_paginated,
			'last_page': last_page,
			'first_page': first_page,			
		}, [custom_proc])	
		
		return HttpResponse(t.render(c)) 


def profile(request, id_author=None):	
	"""
	data for render public profile page
	"""	
	if id_author:
		obj_author = UserProfile.get_entry(user_id=id_author)
		obj_user = UserProfile.get_entry(user_id=id_author)

		if obj_author.is_active == 0:
			obj_author_is_active = True
		else: 
			obj_author_is_active = False

		t = loader.get_template('page_profile.html')
		c = RequestContext(request, {
			'obj_author': obj_author,
		}, [custom_proc])	
		
		return HttpResponse(t.render(c)) 		


def search_record(request):	
	"""
	data for render search record page
	"""	
	if request.method == "POST":
		result = False
		record = request.POST.get('record', '')	
		record_list = Diary.get_search_records(record=record)

		record_list_obj = [{k: v for k, v in record_list}]

		if len(record_list) > 0:
			record_list_obj = [{k: v for k, v in record_list}]
		else:
			record_list_obj = None		

		return HttpResponse(json.dumps(record_list_obj), content_type='application/json')		

	t = loader.get_template('page_search_record.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 		


def most_popular_authors(request):	
	"""
	data for render popular author page. paginated
	"""	
	popular_authors = UserProfile.get_popular_authors_entries()

	paginator = Paginator(popular_authors, 6)
	list_pages = paginator.page_range

	page = request.GET.get('page')
	try:
		popular_authors_paginated = paginator.page(page)
	except PageNotAnInteger:
		popular_authors_paginated = paginator.page(1)
	except EmptyPage:
		popular_authors_paginated = paginator.page(paginator.num_pages)	

	last_page = list_pages[-1]	
	first_page = list_pages[0]		

	t = loader.get_template('page_most_popular_authors.html')
	c = RequestContext(request, {
		'popular_authors': popular_authors,
		'list_pages': list_pages,
		'popular_authors_paginated': popular_authors_paginated,
		'last_page': last_page,
		'first_page': first_page,			
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 


def last_records(request):	
	"""
	data for render last records page. with ajax more-button
	"""	
	count_new_records= Diary.get_count_diary_entries()

	if request.method == 'POST' and request.is_ajax():	
		page_new_records = int(request.POST.get('page_new_records', ''))
		count_new_records = int(request.POST.get('count_new_records', ''))

		new_records = Diary.get_new_diary_entries(cut_begin=page_new_records, cut_end=page_new_records + 6)

		result = serializers.serialize('json', new_records)

		return HttpResponse(json.dumps(result), content_type='application/json')	
	else:
		new_records = Diary.get_new_diary_entries(cut_begin=0, cut_end=6)

		t = loader.get_template('page_last_records.html')
		c = RequestContext(request, {
			'new_records': new_records,
			'count_new_records': count_new_records,
		}, [custom_proc])	
		
		return HttpResponse(t.render(c)) 	


def new_authors(request):	
	"""
	data for render new authors/diary page. with ajax more-button
	"""		
	count_new_authors = UserProfile.get_count_authors_entries()

	if request.method == 'POST' and request.is_ajax():	
		page_new_authors = int(request.POST.get('page_new_authors', ''))
		count_new_authors = int(request.POST.get('count_new_authors', ''))

		new_authors = UserProfile.get_new_authors_entries(cut_begin=page_new_authors, cut_end=page_new_authors + 6)

		result = serializers.serialize('json', new_authors)

		return HttpResponse(json.dumps(result), content_type='application/json')	
	else:
		new_authors = UserProfile.get_new_authors_entries(cut_begin=0, cut_end=6)

		t = loader.get_template('page_new_authors.html')
		c = RequestContext(request, {
			'new_authors': new_authors,
			'count_new_authors': count_new_authors,
		}, [custom_proc])	
		
		return HttpResponse(t.render(c)) 			


@login_required
def my_records(request):	
	"""
	data for render private my records. paginated
	"""		
	all_user_entries = Diary.get_all_user_entries(user_id=request.user.pk)

	paginator = Paginator(all_user_entries, 6)
	list_pages = paginator.page_range

	page = request.GET.get('page')
	try:
		all_user_entries_paginated = paginator.page(page)
	except PageNotAnInteger:
		all_user_entries_paginated = paginator.page(1)
	except EmptyPage:
		all_user_entries_paginated = paginator.page(paginator.num_pages)	

	last_page = list_pages[-1]	
	first_page = list_pages[0]				

	t = loader.get_template('page_my_records.html')
	c = RequestContext(request, {
		'all_user_entries': all_user_entries,
		'list_pages': list_pages,
		'all_user_entries_paginated': all_user_entries_paginated,
		'last_page': last_page,
		'first_page': first_page,		
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


@login_required
def add_records(request):	
	"""
	data for render private add my record
	"""		
	form = addMessageForm()

	if request.method == "POST":
		form = addMessageForm(request.POST)

		if form.is_valid():
			Diary.objects.create(
				user_id=request.user.pk, 
				title=form.cleaned_data.get('title').strip(), 
				date=form.cleaned_data.get('date'), 
				text=form.cleaned_data.get('text').strip(), 
			)

			return HttpResponseRedirect('/my_records/')

	t = loader.get_template('page_add_records.html')
	c = RequestContext(request, {
		'form': form,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


@login_required
def edit_records(request, id_record):	
	"""
	data for render private edit my record
	"""		
	entry = Diary.get_entry(id_record=id_record, user_id=request.user.pk)
	form = addMessageForm(instance=entry)

	if request.method == 'POST':
		form = addMessageForm(request.POST, request.FILES, instance=entry)
		if form.is_valid():		
			form.save()		
			return HttpResponseRedirect('/my_records/')

	t = loader.get_template('page_edit_records.html')
	c = RequestContext(request, {
		'form': form,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 		


@login_required
def change_avatar(request):	
	"""
	data for render private change avatar page
	"""		
	entry_user_profile = UserProfile.get_entry(user_id=request.user.id)	
			
	avatar = entry_user_profile.avatar					
	form = ChangeAvatarForm(instance=entry_user_profile)		
				
	if request.method == 'POST' and request.is_ajax():																
		form = ChangeAvatarForm(request.POST, request.FILES, instance=entry_user_profile)
		if form.is_valid():				
			form.save()	

			filename = False
			if request.FILES:
				filename = True
					
			data = {'filename': filename}	
			return HttpResponse(json.dumps(data), content_type='application/json')			
        		
	t = loader.get_template('page_change_avatar.html')
	c = RequestContext(request, {
		'form': form,
		'avatar': avatar,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


@login_required
def delete_record(request):		
	"""
	data for render private delete record page
	"""			
	if request.method == 'POST' and request.is_ajax():	
		data = {'result': False}		
		id_delete = request.POST.get('id_delete', '')	

		try:
			Diary.delete_entry(id_delete=id_delete, user_id=request.user.pk)	
		except:
			pass
		else:												
			data = {'result': True}	

		return HttpResponse(json.dumps(data), content_type='application/json')			
        		
	t = loader.get_template('my_records.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


@login_required
def active_record(request):		
	"""
	data for render private change public acceess record
	"""			
	if request.method == 'POST' and request.is_ajax():	
		data = {'result': False}		
		id_rec = request.POST.get('id_rec', '')	

		result = Diary.active_entry(id_rec=id_rec, user_id=request.user.pk)													
		data = {'result': result}	

		return HttpResponse(json.dumps(data), content_type='application/json')			
        		
	t = loader.get_template('my_records.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 			


@login_required
def change_password(request):	
	"""
	data for render private change password
	"""		
	form = ChangePasswordForm(request=request)		

	if request.method == 'POST':								
		form = ChangePasswordForm(request.POST, request=request)
		if form.is_valid():
			username = User.objects.get(username__exact=request.user.username)
			username.set_password(form.cleaned_data.get('password1'))
			username.save()	
			return HttpResponseRedirect('/accounts/changed_password/')											

	t = loader.get_template('page_change_password.html')
	c = RequestContext(request, {
		'form': form,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 					


@login_required
def change_profile(request):
	"""
	data for render private change profile
	"""		
	entry_user_profile = UserProfile.get_entry(user_id=request.user.id)	

	avatar = entry_user_profile.avatar
	form = ProfileForm(instance=entry_user_profile)
	
	if request.method == "POST" and request.is_ajax():
		form = ProfileForm(request.POST, instance=entry_user_profile)
		if form.is_valid():
			form.save()

			data = {
				'result': True,	
			}

		return HttpResponse(json.dumps(data), content_type='application/json')	
		
	t = loader.get_template('page_change_profile.html')
	c = RequestContext(request, {
		'form': form, 
		'avatar': avatar, 
	}, [custom_proc])	

	return HttpResponse(t.render(c)) 	


def privacy_policy(request):	
	"""
	template for private policy page
	"""		
	t = loader.get_template('page_privacy_policy.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def page_error404(request):	
	t = loader.get_template('page_error404.html')
	c = RequestContext(request, {}, [custom_proc])	
	return HttpResponse(t.render(c))

