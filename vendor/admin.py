from django.contrib import admin
from .models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user' , 'vendor_name' , 'vendor_license' , 'created_at','is_approved')
    list_display_links = ('user' , 'vendor_name')
    list_editable =('is_approved',)
'''
    #- means descending order
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
'''
admin.site.register(Vendor,VendorAdmin)