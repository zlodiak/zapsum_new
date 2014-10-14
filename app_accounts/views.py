from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import re
import os
from django.conf import settings

from app_accounts.forms import RegistrationForm, AuthenticationCustomForm


def custom_proc(request):
	"""
	request object for every pages
	"""			
	return{
		'request': request,
	}


def registration(request):
	"""
	data for render registration page
	"""			
	form = RegistrationForm()
	
	if request.method == 'POST':
		form = RegistrationForm(request.POST)	
		if form.is_valid():
			new_user = form.save()
			
			return HttpResponseRedirect("/accounts/authentication/")
		
		
	t = loader.get_template('page_registration.html')
	c = RequestContext(request, {
		'form': form, 
	}, [custom_proc])	
	return HttpResponse(t.render(c)) 


def registration_success(request):	
	"""
	tpl for ok registration
	"""		
	t = loader.get_template('page_registration_success.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def authentication(request):
	"""
	data for render authentication page
	"""		
	form = AuthenticationCustomForm()	

	if(request.method == "POST"):
		form = AuthenticationCustomForm(data=request.POST)		
		if form.is_valid():			
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')

			user = auth.authenticate(username=username, password=password)

			if user is not None and user.is_active and username != 'admin':
				auth.login(request, user)
				return HttpResponseRedirect("/")
                	
	t = loader.get_template('page_authentication.html')
	c = RequestContext(request, {
		'form': form, 
	}, [custom_proc])	
	return HttpResponse(t.render(c)) 	


def authentication_success(request):	
	"""
	tpl for ok authentication
	"""		
	t = loader.get_template('page_authentication_success.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def logout(request):
	"""
	logout
	"""		
	auth.logout(request)
	t = loader.get_template('page_logout.html')
	c = RequestContext(request, {}, [custom_proc])	
	return HttpResponse(t.render(c)) 


@login_required
def changed_password(request):	
	"""
	tpl for ok change password
	"""			
	t = loader.get_template('page_changed_password.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 		


def ajax_login_check(request):
	error_login = False
	error_message_login = ''
	error_pass = False
	error_message_pass = ''	
	error_active = False
	error_message_active = ''		

	if request.method == "POST" and request.is_ajax():
		username = request.POST.get('username', '')		
		password = request.POST.get('password', '')		

		#login check unique
		username_req = User.objects.filter(username=username)				

		if not username_req.exists():
			error_login = True
			error_message_login = 'Неверный логин'

		#login check active
		username_req = User.objects.filter(username=username, is_active=1)	

		if not username_req.exists():
			error_active = True
			error_message_active = 'Профиль отключен'			

		#min_length check
		if(len(username) < 3):
			error_login = True
			error_message_login = 'Имя должно состоять не менее чем из 3 символов'

		#max_height check				
		if(len(username) > 30):
			error_login = True
			error_message_login = 'Имя должно состоять не более чем из 30 символов'

		#password check
		user = auth.authenticate(username=username, password=password)
		if user:
			pass
		else:
			error_pass = True
			error_message_pass = 'Неверный пароль'
		logout(request)

		#password min_length check
		if(len(password) < 3):
			error_pass = True
			error_message_pass = 'Пароль должен состоять не менее чем из 6 символов'	

		#password max_height check
		if(len(password) > 30):
			error_pass = True
			error_message_pass = 'Пароль должен состоять не более чем из 30 символов'		

	data = {
		'error_login': error_login,
		'error_message_login': error_message_login,
		'error_pass': error_pass,
		'error_message_pass': error_message_pass,		
		'error_active': error_active,
		'error_message_active': error_message_active,		
	}

	return HttpResponse(json.dumps(data), content_type='application/json')				

	
def delete_profile(request):
	"""
	delete profile. change is_delete in DB. to do cron delete entries(month period)
	"""			
	result = False

	if request.method == "POST" and request.is_ajax():
		username = request.user.username	

		try:
			entry = User.objects.get(username=username)	
			entry.is_active = 0
			entry.save()
		except:
			pass
		else:
			result = True
			auth.logout(request)

	data = {
		'result': result,		
	}

	return HttpResponse(json.dumps(data), content_type='application/json')					