from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from app_accounts.models import UserProfile

class ChangePasswordForm(forms.Form):
	password_old = forms.CharField(
		max_length=30, 
		widget=forms.PasswordInput(),
		label = 'Действующий пароль',
	)
	password1 = forms.CharField(
		widget=forms.PasswordInput(),
		label = 'Новый пароль',
	)
	password2 = forms.CharField(
		widget=forms.PasswordInput(),
		label = 'Новый пароль ещё раз',
	)	

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ChangePasswordForm, self).__init__(*args, **kwargs)		
		
	def clean_password1(self):
		password1 = self.cleaned_data['password1']
		q_letters = len(password1)
		if q_letters < 3:
			raise forms.ValidationError("Пароль не может быть короче 3 символов.")		

		if q_letters > 30:
			raise forms.ValidationError("Пароль не может быть длиннее 30 символов.")					

		return password1		
	
	def clean_password_old(self):
		cleaned_data = self.cleaned_data
		password_old = cleaned_data.get("password_old")	
		if not self.request.user.check_password(password_old):
			raise forms.ValidationError("Действующий пароль введён не верно.")
		else:
			return password_old
	
	def clean(self):	
		cleaned_data = self.cleaned_data
		password1 = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")	
        		
		if password1 != password2:		
			raise forms.ValidationError("Новые пароли не совпадают.")
		else:							
			return cleaned_data


class ChangeAvatarForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = (
			'avatar', 
		)			