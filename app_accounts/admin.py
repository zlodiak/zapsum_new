from django.contrib import admin
from app_accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	fields = ['gender', 'phone', 'skype', 'email', 'other', 'avatar', ]	
	
	class Meta:
		verbose_name = 'Профиль пользователя'
		verbose_name_plural = 'Профиль пользователя'	

admin.site.register(UserProfile, UserProfileAdmin)		