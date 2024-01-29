from django.shortcuts import render,redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order
import simplejson as json
from .utils import generate_order_number
import razorpay
from foodOnline_main.settings import RZP_KEY_ID , RZP_KEY_SECRET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from .models import Payment,OrderedFood
from accounts.utils import send_notification
from vendor.models import Vendor
from menu.models import FoodItem
# Create your views here.

client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))
def place_order(request):
    cartitems=Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_count=cartitems.count()
    if cart_count<=0:
        return redirect('marketplace')
    
    #Getting Unique Vendors Ids
    vendors_ids =[] 
    for i in cartitems:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)

    #{'vendor_id':{'subtotal':{'tax_type':{'tax_percentage':'tax_amount'}}}}        
    subtotal=0

    for i in cartitems:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id , vendor_id__in=vendors_ids)
        print(fooditem,fooditem.vendor.id)
        subtotal+=(fooditem.price * i.quantity )
        print(subtotal)
    #print(vendors_ids)
    
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
            #Many to Many Relationship of vendor attribute in order model
            order.vendor.add(*vendors_ids)
            order.save()
            print('test1')
            #RazorPay Payment - from docs of razor pay
            DATA={
                "amount": float(order.total) * 100,
                "currency": "INR",
                "receipt": "receipt#"+order.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                }
            }
            #order will be created in razorpay server
            rzp_order = client.order.create(data=DATA)
            rzp_order_id = rzp_order['id']
            #print(rzp_order)
            

            context={
                'order':order,
                'cartitems':cartitems,
                'rzp_order_id':rzp_order_id,
                'RZP_KEY_ID':RZP_KEY_ID,
            }
            return render(request,'orders/place_order.html',context)

        else:
            print(form.errors)
    return render(request,'orders/place_order.html')


def payments(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        #store payment details in payment model
        print('Test')
        transaction_id = request.POST.get('transaction_id') 
        print(transaction_id)
        order_number = request.POST.get('order_number')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order=Order.objects.get(user=request.user , order_number=order_number)
        print(order)

        payment=Payment(
            user=request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount=order.total,
            status=status
        )

        print(payment)
        payment.save()

        
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        #MOVE THE CART ITEMS TO ORDERED FOOD MODEL

        cart_items=Cart.objects.filter(user=request.user)
        print(cart_items)
        for item in cart_items:
            ordered_food=OrderedFood()
            ordered_food.order=order
            ordered_food.payment=payment
            ordered_food.user=request.user
            ordered_food.fooditem=item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price=item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity #total amount
            ordered_food.save()
            #print(ordered_food)

        #SEND CONFIRMATION EMAILTO THE USER
        #coming from accounts.utils
        mail_subject = 'Thank You for Ordering from us'
        mail_template='orders/order_confirmation_email.html'
        context={
            'user':request.user,
            'order':order,
            'to_email':order.email
        }
        send_notification(mail_subject , mail_template , context)
        

        
        #SEND ORDER RECEIVED EMAIL TO VENDOR

        mail_subject='You have received a new order'
        mail_template='orders/new_order_received.html'
        #Multiple email address to be passed in list
        to_emails=[]
        for i in cart_items:
            if i.fooditem.vendor.user.email  not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)
        print('Test environmeny',to_emails)
        context={
            'order':order,
            'to_email':to_emails,
        }


        send_notification(mail_subject,mail_template,context)

        #CLEAR THE CART IF PAYMENT IS SUCCESS
        cart_items.delete()
        #return HttpResponse('Data Saved and Mail sent')
    
        #RETURN BACK TO AJAX IF SUCCESS OF FAILURE - SEND TRANSACTION FUNCTION
        response={
            'order_number':order_number,
            'transaction_id':transaction_id,
        }
        return JsonResponse(response)
    return HttpResponse('Payment View')
##########GETTING ISSUE HERE#######################################3
def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    
    try:
        order=Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)

        subtotal=0

        for items in ordered_food:
            subtotal +=(items.price * items.quantity)

        #tax_data = json.loads(order.tax_data)
        #print(tax_data)
        context={
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
        }

        return render(request,'orders/order_complete.html',context)
    except:
        return redirect('home')
   









