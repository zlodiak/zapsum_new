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
	return{
		'request': request,
	}


def registration(request):
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
	t = loader.get_template('page_registration_success.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def authentication(request):
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
	t = loader.get_template('page_authentication_success.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def logout(request):
	auth.logout(request)
	t = loader.get_template('page_logout.html')
	c = RequestContext(request, {}, [custom_proc])	
	return HttpResponse(t.render(c)) 


@login_required
def changed_password(request):	
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


def ajax_registration_check(request):
	error_login = False
	error_message_login = ''
	error_email = False
	error_message_email = ''	
	error_password1 = False
	error_message_password1 = ''
	error_password2 = False
	error_message_password2 = ''			

	if request.method == "POST" and request.is_ajax():
		username = request.POST.get('username', '')		
		email = request.POST.get('email', '')		
		password1 = request.POST.get('password1', '')	
		password2 = request.POST.get('password2', '')			

		#login check unique
		username_req = User.objects.filter(username=username)				

		if username_req.exists():
			error_login = True
			error_message_login = 'Логин занят'

		#login min_length check
		if(len(username) < 3):
			error_login = True
			error_message_login = 'Имя должно состоять не менее чем из 3 символов'

		#login  max_height check				
		if(len(username) > 30):
			error_login = True
			error_message_login = 'Имя должно состоять не более чем из 30 символов'

		#email check unique
		email_req = User.objects.filter(email=email)				

		if email_req.exists():
			error_email = True
			error_message_email = 'Email занят'		

		#email regex check
		EMAIL_REGEX = re.compile(r'.*?@.*?\..*?$')
		if not EMAIL_REGEX.match(email):
			error_email = True
			error_message_email = 'Введите корректный email'

		#email min_length check
		if(len(email) < 6):
			error_email = True
			error_message_email = 'Email должен состоять не менее чем из 6 символов'

		#email max_height check				
		if(len(email) > 30):
			error_email = True
			error_message_email = 'Email должен состоять не более чем из 30 символов'	

		#password1 min_length check
		if(len(password1) < 6):
			error_password1 = True
			error_message_password1 = 'Пароль должен состоять не менее чем из 6 символов'

		#password1 max_height check				
		if(len(password1) > 30):
			error_password1 = True
			error_message_password1 = 'Пароль должен состоять не более чем из 30 символов'		

		#password2 compare check				
		if(password1 != password2):
			error_password2 = True
			error_message_password2 = 'Пароли должны совпадать'						

	data = {
		'error_login': error_login,
		'error_message_login': error_message_login,	
		'error_email': error_email,
		'error_message_email': error_message_email,			
		'error_password1': error_password1,
		'error_message_password1': error_message_password1,			
		'error_password2': error_password2,
		'error_message_password2': error_message_password2,			
	}

	return HttpResponse(json.dumps(data), content_type='application/json')				

	
def delete_profile(request):
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