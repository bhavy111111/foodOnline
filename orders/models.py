from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
import simplejson as json
# Create your models here.

request_object=''
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
    #Many to  Many Relationship
    vendor=models.ManyToManyField(Vendor,blank=True)
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
    #total data will be carrying every attribute subtotal tax related to every vendor
    total_data = models.JSONField(blank=True,null=True)

    total_tax=models.FloatField()
    payment_method=models.CharField(max_length=25)
    status=models.CharField(max_length=15,choices=STATUS,default='New')
    is_ordered = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #concat fiirst and last name

    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def order_placed_to(self):
        return ",".join([str(i) for i in self.vendor.all()])
    
    def get_total_by_vendor(self):
        vendor=Vendor.objects.get(user=request_object.user)
        subtotal = 0
        tax=0
        tax_dict={}
        if self.total_data:
            total_data = json.loads(self.total_data)
            data = total_data.get(str(vendor.id))
            print('data inside',data)
            #print(data)

           
            for key,val in data.items():
                subtotal+=float(key)
                #val=val.replace("'",'"')
                val=json.loads(val)
                
                tax_dict.update(val)

                #calculate tax for vendor dashboard

                for i in val:
                    for j in val[i]:
                        tax+=float(val[i][j])
        grand_total = float(subtotal)+ float(tax)
        print('tax_dict',tax_dict)
        print('subtotal',subtotal)
        print('tax',tax)
        print('grand_total',grand_total)

        context={
            'grand_total':grand_total,
        }

        
        #a = vendor.id
        # if self.total_data:
        #     print('Models Test',self.total_data)
        #     #total_data=json.dumps(self.total_data)
        #     data=self.total_data.get(8)
        #     print(data)
        #     #print(total_data)
        return vendor
    
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

    




