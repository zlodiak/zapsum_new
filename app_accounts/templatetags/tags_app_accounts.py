from django import template
from django.contrib.auth.models import User
from django.http import HttpResponse

from app_messages.models import Message

register = template.Library()
	
	
@register.inclusion_tag("part_auth_area.html")
def part_auth_area(user):
	if user:
		return {
			'is_authenticated': user.is_authenticated,
			'username': user.username,
			'user_id': user.pk,
		}	

@register.inclusion_tag("part_nav_area.html")
def part_nav_area(user):
	if user:
		new_sends = Message.get_new_sends(user.pk)

		return {
			'is_authenticated': user.is_authenticated,
			'new_sends': new_sends,
		}	



		

	


