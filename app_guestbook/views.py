from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render, render_to_response

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

	if request.method == "POST":
		form = GuestbookRecordForm(request.POST)	

		if form.is_valid():
			GuestbookRecord.objects.create(
				username=form.cleaned_data.get('username').strip(), 
				text=form.cleaned_data.get('text').strip(), 
				is_active=True,
			)	

			return HttpResponseRedirect('/guestbook/?action=2')		

	guestbook_records = GuestbookRecord.get_all_entries()
		
	t = loader.get_template('page_guestbook_tape.html')
	c = RequestContext(request, {
		'guestbook_records': guestbook_records,
		'form': form,
		'action': action,
	}, [custom_proc])	
	return HttpResponse(t.render(c)) 


			