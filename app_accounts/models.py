from django.db import models
from django.contrib.auth.models import User, UserManager


class Gender(models.Model):		
	gender = models.CharField(
		max_length=10, 
		blank=True,
	)	

	def __str__(self):
		return self.gender	


class UserProfile(User):			
	gender = models.ForeignKey(
		Gender,
		verbose_name='Пол',
		blank=True,
		null=True,
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