from django.db import models
from django.contrib.auth.models import User, UserManager


class UserProfile(User):
	CHOICES_gender = (
		('0', 'М', ),
		('1', 'Ж', ),
	)
		
	nickname = models.CharField(
		max_length=50, 
		blank=False,
	)		
	gender = models.CharField(
		max_length=10, 
		choices=CHOICES_gender, 
		blank=False,
	)
	phone = models.CharField(
		max_length=50, 
		blank=False,
	)
	skype = models.CharField(
		max_length=50, 
		blank=False,
	)	
	other = models.TextField(
		max_length=500,
		blank=False,
	)
	avatar = models.ImageField(
		upload_to='userprofile/', 
		blank=False,
	)
	
	objects = UserManager()