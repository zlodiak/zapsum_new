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
from app_accounts.models import UserProfile
from app_zapsum.models import Diary
from app_zapsum.forms import ChangePasswordForm, ChangeAvatarForm, addMessageForm

def custom_proc(request):
	return{
		'request': request,
	}


def rules(request):	
	t = loader.get_template('page_rules.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def search_author(request):	
	if request.method == "POST":
		result = False
		author = request.POST.get('author', '')	
		authors_list = UserProfile.get_search_authors_entries(author)

		result = serializers.serialize("json", authors_list)
		return HttpResponse(json.dumps(result), content_type='application/json')		

	t = loader.get_template('page_search_author.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def search_record(request):	
	t = loader.get_template('page_search_record.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 		


def most_popular_authors(request):	
	t = loader.get_template('page_most_popular_authors.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 		


def last_records(request):	
	t = loader.get_template('page_last_records.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def new_authors(request):	
	new_authors = UserProfile.get_new_authors_entries()

	t = loader.get_template('page_new_authors.html')
	c = RequestContext(request, {
		'new_authors': new_authors,
	}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 			


@login_required
def my_records(request):	
	all_user_entries = Diary.get_all_user_entries(id=request.user.pk)

	paginator = Paginator(all_user_entries, 3)
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
	entry_user_profile = UserProfile.objects.get(user_ptr_id=request.user.id)	
			
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
	entry_user_profile = UserProfile.objects.get(user_ptr_id=request.user.id)		
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
	t = loader.get_template('page_privacy_policy.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


