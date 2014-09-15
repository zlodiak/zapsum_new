from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
import re

from app_accounts.models import UserProfile


class registrationForm(UserCreationForm):	
	username = forms.EmailField(
		label='Email',
		help_text='',
		max_length=50, 
		required=True,
	)	

	nickname = forms.CharField(
		label='Отображаемое имя',
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
			'nickname',    
			'password1', 
			'password2',
		)

	def clean_password1(self):
		password1 = self.cleaned_data['password1']
		q_letters = len(password1)
		if q_letters < 6:
			raise forms.ValidationError("Пароль не может быть короче 6 символов.")		

		return password1	
		
	def clean_nickname(self):
		nickname = self.cleaned_data['nickname']
		q_letters = len(nickname)
		if q_letters < 3:
			raise forms.ValidationError("Логин не может быть короче 3 символов.")		

		return nickname		

	def clean_username(self):
		username = self.cleaned_data['username']
		if username == 'www@www.ru':
			pass
		else:
			raise forms.ValidationError("Введите корректный email.")

		return username		


class authenticationCustomForm(AuthenticationForm):
	username = forms.CharField(
		label='Email',
		widget=forms.TextInput(),		
	)

	password = forms.CharField(
		label='Пароль', 
		widget=forms.PasswordInput(),
	)
