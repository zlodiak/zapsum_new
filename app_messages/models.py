from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):		
	"""
	class for messages
	"""	
	sender = models.ForeignKey(
		User,
		verbose_name='Отправитель',
		related_name='sender',
		blank=False,
		null=False,
	)	
	reciever = models.ForeignKey(
		User,
		verbose_name='Получатель',
		related_name='recipient',
		blank=False,
		null=False,	
	)	
	date_send = models.DateTimeField(
		auto_now_add=True,
		blank=False,
		null=False,		
	)
	date_recieve = models.DateTimeField(
		blank=True,
		null=True,			
	)	
	theme = models.CharField(
		'Тема сообщения',
		max_length=200, 
		blank=False,
		null=True,
	)		
	text = models.TextField(
		'Текст сообщения',
		max_length=10000, 
		blank=False,
	)
	sender_show = models.BooleanField(
		default=True,
	)	
	reciever_show = models.BooleanField(
		default=True,
	)			

	@classmethod
	def get_sended_messages(self, id):		
		return self.objects.filter(sender=id, sender_show=True).order_by('-date_send')
		
	@classmethod
	def exists_sended_messages(self, id):		
		return self.objects.filter(sender=id, sender_show=True).exists()	
		
	@classmethod
	def get_recieve_messages(self, id):		
		return self.objects.filter(reciever=id, reciever_show=True).order_by('-date_send')
		
	@classmethod
	def exists_recieve_messages(self, id):		
		return self.objects.filter(reciever=id, reciever_show=True).exists()	
		
	@classmethod
	def delete_message(self, delete_id):		
		return self.objects.get(pk=delete_id).delete()	
		
	@classmethod
	def get_message(self, message_id):		
		result = self.objects.get(id=message_id)			
		date_recieve = result.date_recieve
		
		if date_recieve is None:
			result.date_recieve = datetime.datetime.now()
			result.save()
			
		return result
		
	@classmethod
	def get_new_sends(self, user_pk):		
		return self.objects.filter(reciever_show=True, reciever=user_pk, date_recieve__isnull=True).count()


class Modal(models.Model):		
	"""
	class for modal windows
	message: text
	timeout: time before annihilation window
	window: type window(0-smsll, 1-large)
	cancel_button: cancel button visible or not (not used until)
	"""
	message = models.CharField(
		max_length=2000, 
		blank=False,
		null=False,
	)	
	timeout = models.IntegerField(
		blank=False,
		null=False,
	)	
	window = models.IntegerField(
		blank=False,
		null=False,
	)	
	cancel_button = models.BooleanField(
		blank=False,
		null=False,
	)			

	@classmethod
	def get_entries(self):		
		return self.objects.all()

