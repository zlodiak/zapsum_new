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
	last_edit_date = models.DateTimeField(
		'Дата последнего редактирования',
		#default=datetime.now(),
		auto_now=True,
	)	
	is_active = models.BooleanField(default=True)					
	is_delete = models.BooleanField(default=False)					
	
	@classmethod
	def get_all_entries(self):
		return self.objects.all()
		
	@classmethod
	def get_all_user_entries(self, user_id):
		return self.objects.filter(user_id=user_id, is_delete=False).order_by('-date')	
		
	@classmethod
	def delete_entry(self, id_delete, user_id):
		return self.objects.get(id=id_delete, user_id=user_id).delete()	

	@classmethod
	def active_entry(self, id_rec, user_id):
		state = self.objects.get(id=id_rec, user_id=user_id)	

		if state.is_active:
			state.is_active = False
			state.save()
			result = False
		else:
			state.is_active = True
			state.save()
			result = True

		return result		

	@classmethod
	def get_entry(self, id_record, user_id):
		return self.objects.get(id=id_record, user_id=user_id, is_delete=False)		

	@classmethod
	def get_entry_public(self, id_record):
		return self.objects.get(pk=id_record, is_active=True, is_delete=False)	

	@classmethod
	def get_count_diary_entries(self):
		return self.objects.all().count()		

	@classmethod
	def get_new_diary_entries(self, cut_begin=0, cut_end=2):
		return self.objects.filter(is_delete=0, is_active=1)[cut_begin:cut_end]				
			
	@classmethod
	def get_search_records(self, record):
		return self.objects.filter(title__icontains=record, is_active=1).values_list('id', 'title')	


