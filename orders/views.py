from django.shortcuts import render,redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order
import simplejson as json
from .utils import generate_order_number
# Create your views here.

def place_order(request):
    cartitems=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cartitems.count()
    if cart_count<=0:
        return redirect('marketplace')
    
    subtotal=get_cart_amount(request)['subtotal']
    total_tax=get_cart_amount(request)['tax']
    grand_total=get_cart_amount(request)['grand_total']
    tax_data=get_cart_amount(request)['tax_dict']
    print(tax_data)
    #print(subtotal,total_tax,grand_total,tax_data)

    #Updating the value which we are getting placeorder
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            #print(form.cleaned_data)
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.pincode = form.cleaned_data['pincode']
            order.user = request.user
            order.total = grand_total
            order.tax_date = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method='RazorPay'
            
            #print('Results previous before going to db',order)
            order.save() #order.id is generated after when value hits to the database
            order.order_number = generate_order_number(order.id)
            order.save()
            return redirect('place_order')

         
        else:
            print(form.errors)
    return render(request,'orders/place_order.html')