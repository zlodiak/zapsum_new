from django.db import models
from datetime import datetime  

class Diary(models.Model):
	user_id = models.IntegerField(
		'',
		blank=True,
		null=True,		
	)		
	title = models.CharField(
		'Заголовок записи',
		max_length=100, 
		blank=False,
	)			
	date = models.DateField(
		'Дата записи',
		blank=True,
		null=True,
	)						
	text = models.TextField(
		'Содержание записи',
		max_length=5000, 
		blank=False,
	)	
	last_edit_date = models.DateField(
		'Дата последнего редактирования',
		default=datetime.now(),
	)	
	is_active = models.BooleanField(default=True)					
	is_delete = models.BooleanField(default=False)					
	
	@classmethod
	def get_all_entries(self):
		return self.objects.all()
		
	@classmethod
	def get_all_user_entries(self, id):
		return self.objects.filter(user_id=id)		
		
	@classmethod
	def delete_entry(self, id_delete, user_id):
		return self.objects.get(id=id_delete, user_id=user_id).delete()	

	@classmethod
	def get_entry(self, id_record, user_id):
		return self.objects.get(id=id_record, user_id=user_id)			



