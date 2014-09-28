from django.db import models
from django.contrib.auth.models import User, UserManager
from sorl.thumbnail import ImageField


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
		upload_to='userprofile/avatar/', 
		blank=True,
		null=True,
	)
	
	objects = UserManager()

	@classmethod
	def get_search_authors_entries(self, author):
		#return self.objects.filter(username__icontains=author)		
		return self.objects.filter(username__icontains=author)	

	@classmethod
	def get_new_authors_entries(self):
		return self.objects.filter(is_active=1, is_superuser=0).order_by('-date_joined')			