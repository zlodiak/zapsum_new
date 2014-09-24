from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.contrib.auth.models import User
from sorl.thumbnail import delete
import json

from app_accounts.forms import ProfileForm
from app_accounts.models import UserProfile
from app_zapsum.forms import ChangePasswordForm, ChangeAvatarForm

def custom_proc(request):
	return{
		'request': request,
	}


def rules(request):	
	t = loader.get_template('page_rules.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def search_author(request):	
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
	t = loader.get_template('page_new_authors.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 			


@login_required
def my_records(request):	
	t = loader.get_template('page_my_records.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


@login_required
def add_records(request):	
	t = loader.get_template('page_add_records.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


@login_required
def change_avatar(request):	
	entry_user_profile = UserProfile.objects.get(user_ptr_id=request.user.id)	
			
	avatar = entry_user_profile.avatar					
	form = ChangeAvatarForm(instance=entry_user_profile)		
				
	if request.method == 'POST' and request.is_ajax():								
	#if request.method == 'POST':								
		form = ChangeAvatarForm(request.POST, request.FILES, instance=entry_user_profile)
		if form.is_valid():				
			form.save()	
			#return HttpResponseRedirect('/change_avatar/')		
			data = {'txt': 'Загрузили'}
			return HttpResponse(json.dumps(data), content_type='application/json')			
        		
	t = loader.get_template('page_change_avatar.html')
	c = RequestContext(request, {
		'form': form,
		'avatar': avatar,
	}, [custom_proc])	
	
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

			return HttpResponse()	
		
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


