from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response


def custom_proc(request):
	return{
		'request': request,
	}


def rules(request):	
	t = loader.get_template('app_zapsum/page_rules.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 	


def search_author(request):	
	t = loader.get_template('app_zapsum/page_search_author.html')
	c = RequestContext(request, {}, [custom_proc])	
	
	return HttpResponse(t.render(c)) 		