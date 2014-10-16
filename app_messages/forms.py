from django import forms
from django.forms import ModelForm

from app_messages.models import Message


error_dict = {
	'spaces': 'Поле не может состоять только из пробелов',
}


class MessageForm(forms.ModelForm):				
	class Meta:
		model = Message
		fields = (
			'theme', 
			'text', 
		)
		
	def clean_text(self):
		text = self.cleaned_data['text'].strip()
		if len(text) == 0:
			raise forms.ValidationError(error_dict['spaces'])		

		return text		