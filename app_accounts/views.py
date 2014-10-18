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