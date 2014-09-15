from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

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
		label='Подтверждение пароля:',
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


class authenticationCustomForm(AuthenticationForm):
	username = forms.CharField(
		label='Email',
		widget=forms.TextInput(),		
	)

	password = forms.CharField(
		label='Пароль', 
		widget=forms.PasswordInput(),
	)
