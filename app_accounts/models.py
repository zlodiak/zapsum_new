# -*- coding:utf-8 -*-

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

	@classmethod
	def get_entry(self, gender_id):
		result = Gender.objects.get(id=gender_id)
		return result			


class UserProfile(User):			
	gender = models.ForeignKey(
		Gender,
		verbose_name='Пол',
		blank=True,
		null=True,
	)
	nickname = models.CharField(
		'Отображаемое имя',
		max_length=50, 
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
		upload_to='userprofile/avatar/', 
		blank=True,
		null=True,
	)
	views = models.IntegerField(
		default=0,
		null=False,
		blank=True,
	)	
	
	objects = UserManager()

	@classmethod
	def get_new_authors_entries(self, cut_begin=0, cut_end=2):
		return self.objects.filter(is_active=1, is_superuser=0)[cut_begin:cut_end]	

	@classmethod
	def get_count_authors_entries(self):
		return self.objects.filter(is_active=1, is_superuser=0).count()	

	@classmethod
	def get_entry(self, user_id):
		result = UserProfile.objects.get(user_ptr_id=user_id)
		return result	

	@classmethod
	def get_popular_authors_entries(self):
		return self.objects.filter(is_active=1, is_superuser=0).order_by('-views')		

	@classmethod
	def get_authors_list(self, author):
		result = UserProfile.objects.filter(nickname__icontains=author, is_active=1, is_superuser=0).values_list('user_ptr_id', 'nickname')	
		return result					
	
	
	