from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from app_guestbook.models import GuestbookRecord


error_dict = {
	'spaces': 'Поле не может состоять только из пробелов',
}


class GuestbookRecordForm(forms.ModelForm):				
	class Meta:
		model = GuestbookRecord
		fields = (
			'username', 
			'text', 
		)
		
	def clean_username(self):
		username = self.cleaned_data['username'].strip()
		if len(username) == 0:
			raise forms.ValidationError(error_dict['spaces'])		

		return username		

	def clean_text(self):
		text = self.cleaned_data['text'].strip()
		if len(text) == 0:
			raise forms.ValidationError(error_dict['spaces'])		

		return text			
