from django.db import models
from accounts.models import User
from menu.models import FoodItem
# Create your models here.
class Payment(models.Model):
    PAYMENT_METHOD = (
        ('RazorPay','RazorPay'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_id= models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD , max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    
class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,blank=True,null=True,on_delete=models.SET_NULL)
    order_number = models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100,blank=True)
    email=models.EmailField(max_length=100)
    address=models.CharField(max_length=100)
    country=models.CharField(max_length=100,blank=True) 
    state=models.CharField(max_length=15,blank=True)
    city=models.CharField(max_length=50)
    pincode=models.CharField(max_length=10)
    total = models.FloatField()
    #tax_data will be json field - Tax is more than 1 thats y dict
    tax_data = models.JSONField(blank=True,help_text="Data format :{'tax_type':{'tax_percentage':'tax_amount'}}",null=True)
    total_tax=models.FloatField()
    payment_method=models.CharField(max_length=25)
    status=models.CharField(max_length=15,choices=STATUS,default='New')
    is_ordered = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #concat fiirst and last name

    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.order_number
    
class OrderedFood(models.Model):
    order=models.ForeignKey(Order , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fooditem=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.fooditem

    




