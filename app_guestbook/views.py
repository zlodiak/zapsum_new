from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app_messages.models import Modal
from app_guestbook.models import GuestbookRecord
from app_guestbook.forms import GuestbookRecordForm


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


def guestbook_tape(request):
	"""
	data for render tape of guestbook page
	"""		
	action = None
	if request.GET.get('action'):
		action = int(request.GET.get('action'))	

	form = GuestbookRecordForm()	

	guestbook_records = GuestbookRecord.get_all_entries()

	paginator = Paginator(guestbook_records, 10)
	list_pages = paginator.page_range
	
	page = request.GET.get('page')
	try:
		guestbook_records_paginated = paginator.page(page)
	except PageNotAnInteger:
		guestbook_records_paginated = paginator.page(1)
	except EmptyPage:
		guestbook_records_paginated = paginator.page(paginator.num_pages)	
		
	last_page = list_pages[-1]	
	first_page = list_pages[0]		

	if request.method == "POST":
		form = GuestbookRecordForm(request.POST)	

		if form.is_valid():
			GuestbookRecord.objects.create(
				username=form.cleaned_data.get('username').strip(), 
				text=form.cleaned_data.get('text').strip(), 
				is_active=True,
			)	

			return HttpResponseRedirect('/guestbook/?action=2')		
		
	t = loader.get_template('page_guestbook_tape.html')
	c = RequestContext(request, {
		'form': form,
		'list_pages': list_pages,
		'guestbook_records_paginated': guestbook_records_paginated,
		'last_page': last_page,
		'first_page': first_page,			
		'action': action,
	}, [custom_proc])	
	return HttpResponse(t.render(c)) 


			