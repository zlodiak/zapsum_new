from django.db import models
from datetime import datetime  


class GuestbookRecord(models.Model):
	username = models.CharField(
		'Имя',
		max_length=100, 
		blank=False,
		null=False,		
	)								
	text = models.TextField(
		'Содержание записи',
		max_length=50000, 
		blank=False,
	)	
	date = models.DateTimeField(
		'Дата создания',
		#default=datetime.now(),
		auto_now=True,
	)	
	is_active = models.BooleanField(default=True)			

	@classmethod
	def get_all_entries(self):
		return self.objects.filter(is_active=True).order_by('-date')				
			
	

