from django.contrib import admin

# Register your models here.
from .models import Payment,Order,OrderedFood

class OrderedFoodInline(admin.TabularInline):
    model=OrderedFood

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','name','phone','email','total','payment_method','status','is_ordered',]

    inlines=[OrderedFoodInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)

