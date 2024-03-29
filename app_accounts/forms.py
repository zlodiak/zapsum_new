from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
import re

from app_accounts.models import UserProfile, Gender

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from captcha.fields import CaptchaField


class RegistrationForm(UserCreationForm):	
	username = forms.CharField(
		label='Логин',
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

	captcha = CaptchaField()

	class Meta:
		model = UserProfile
		fields = (  
			'username',  
			'nickname',    
			'email',    
			'password1', 
			'password2',
		)

	def clean_password1(self):
		password1 = self.cleaned_data['password1']
		q_letters = len(password1)
		if q_letters < 6:
			raise forms.ValidationError("Пароль не может быть короче 6 символов.")		
		if q_letters > 30:
			raise forms.ValidationError("Пароль не может быть длиннее 30 символов.")	

		return password1	
		
	def clean_username(self):
		username = self.cleaned_data['username']
		q_letters = len(username)
		if q_letters < 3:
			raise forms.ValidationError("Логин не может быть короче 3 символов.")		
		if q_letters > 30:
			raise forms.ValidationError("Логин не может быть длиннее 30 символов.")				

		return username		


class AuthenticationCustomForm(AuthenticationForm):
	username = forms.CharField(
		label='Логин',
		widget=forms.TextInput(),		
	)

	password = forms.CharField(
		label='Пароль', 
		widget=forms.PasswordInput(),
	)


class ProfileForm(forms.ModelForm):
	gender = forms.ModelChoiceField(
		queryset=Gender.objects.all(),
		empty_label = None,
		label='Пол',
	)		

	phone = forms.CharField(
		label='Номер телефона',
		widget=forms.TextInput(),	
		required=False,		
	)

	skype = forms.CharField(
		label='Skype',
		widget=forms.TextInput(),	
		required=False,		
	)

	nickname = forms.CharField(
		label='Отображаемое имя',
		widget=forms.TextInput(),	
		required=False,		
	)	

	other = forms.CharField(
		label='Доп.информация',
		widget=SummernoteWidget({
		    'width': '670px',
		    #'height': '200px',	    
		}),	
		required=False,	
	)				

	class Meta:
		model = UserProfile
		fields = (  
			'gender',    
			'phone',    
			'skype',    
			'nickname',    
			'other', 
		)

