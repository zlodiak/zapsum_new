from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from app_messages.models import Message

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


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


class CreateMessageForm(forms.ModelForm):
	text = forms.CharField(
		widget=SummernoteWidget({
		    'width': '670px',
		    #'height': '200px',	    
		}),
	)	

	class Meta:
		model = Message
		fields = (
			'reciever', 
			'theme', 
			'text', 
		)
