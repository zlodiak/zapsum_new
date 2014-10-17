from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse

register = template.Library()
	
	
@register.inclusion_tag("part_pagination.html")
def part_pagination(entries, list_pages, last_page, first_page):
	return {
		'entries_paginated': entries,
		'list_pages': list_pages,
		'last_page': last_page,
		'first_page': first_page,
	}	
	
@register.inclusion_tag("part_modal.html")
def part_modal(modal, action):
	window_type = None
	window_type_label = None
	timeout = None
	message = None

	for entry in modal:
		if action == entry.id:
			if entry.window == 0:
				window_type = 'infoModal'
				window_type_label = 'mySmallModalLabel'
			elif entry.window == 1:	
				window_type = 'commonModal'
				window_type_label = 'commonModalLabel'					

			timeout = entry.timeout	
			message = entry.message

	return {
		'window_type': window_type,
		'window_type_label': window_type_label,
		'timeout': timeout,
		'message': message,
	}
	


