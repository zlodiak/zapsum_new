from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse

register = template.Library()
	
	
@register.inclusion_tag("part_auth_area.html")
def part_auth_area(user):
	return {
		'is_authenticated': user.is_authenticated,
		'username': user.username,
		'user_id': user.pk,
	}	




	

	


