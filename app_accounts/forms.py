from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
import re

from app_accounts.models import UserProfile


class RegistrationForm(UserCreationForm):	
	username = forms.CharField(
		label='Отображаемое имя',
		help_text='',
		max_length=50, 
		required=True,
	)	

	email = forms.EmailField(
		label='Email',
		help_text='',
		required=True,
	)
	
	password1 = forms.CharField(
		label='Пароль',
		help_text='',
		required=True,
		widget=forms.PasswordInput,
	)	
	
	password2 = forms.CharField(
		label='Подтверждение пароля',
		help_text='',
		required=True,
		widget=forms.PasswordInput,
	)	

	class Meta:
		model = UserProfile
		fields = (  
			'username',    
			'email',    
			'password1', 
			'password2',
		)

	def clean_password1(self):
		password1 = self.cleaned_data['password1']
		q_letters = len(password1)
		if q_letters < 6:
			raise forms.ValidationError("Пароль не может быть короче 6 символов.")		

		return password1	
		
	def clean_username(self):
		username = self.cleaned_data['username']
		q_letters = len(username)
		if q_letters < 3:
			raise forms.ValidationError("Логин не может быть короче 3 символов.")		

		return username		


class AuthenticationCustomForm(AuthenticationForm):
	username = forms.CharField(
		label='Отображаемое имя',
		widget=forms.TextInput(),		
	)

	password = forms.CharField(
		label='Пароль', 
		widget=forms.PasswordInput(),
	)

