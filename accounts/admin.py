from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin



class CustomerUserAdmin(UserAdmin):
    list_display = ('email' , 'first_name' , 'last_name' , 'username' , 'role','is_active')
    #- means descending order
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User,CustomerUserAdmin)