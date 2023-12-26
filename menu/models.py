from django.db import models
from vendor.models import Vendor
# Create your models here.

class Category(models.Model):
    #if vendor is deleted particular then this category of vendor will also be deleted
    
    vendor = models.ForeignKey(Vendor , on_delete = models.CASCADE)
    category_name = models.CharField(max_length=50,unique=True)
    #Sea food -  sea-food
    slug = models.SlugField(max_length=50,unique=True)
    description = models.TextField(max_length=250 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category_name}'

class FoodItem(models.Model):

    vendor = models.ForeignKey(Vendor , on_delete = models.CASCADE)
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=250,blank=True)
    price  = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.food_title}'




