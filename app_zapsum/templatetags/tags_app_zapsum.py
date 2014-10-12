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
	

	


