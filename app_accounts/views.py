from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
import json
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
			
			return HttpResponseRedirect("/accounts/registration_success/")
		
		
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
				return HttpResponseRedirect("/accounts/authentication_success/")
                	
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


def ajax_username_check(request):
	error = False
	error_message = ''

	if request.method == "POST" and request.is_ajax():
		username = request.POST.get('username', '')		

		#login check
		username_req = User.objects.filter(username=username)				

		if not username_req.exists():
			error = True
			error_message = 'Неверный логин'

		#min_length check
		if(len(username) < 3):
			error = True
			error_message = 'Имя должно состоять не менее чем из 3 символов'

		#max_height check				
		if(len(username) > 30):
			error = True
			error_message = 'Имя должно состоять не более чем из 30 символов'

	data = {
		'error': error,
		'error_message': error_message,
	}

	return HttpResponse(json.dumps(data), content_type='application/json')	


	