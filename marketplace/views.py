from django.shortcuts import render,get_object_or_404,HttpResponse
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import Cart
from .context_processors import get_cart_counter,get_cart_amount
from django.db.models import Q

def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True , user__is_active=True)
    vendors_count=vendors.count()
    context={
        'vendors':vendors,
        'vendors_count':vendors_count,
    }
    return render(request,'marketplace/listings.html',context)

def vendor_detail(request,vendor_slug):

    vendor = get_object_or_404(Vendor,vendor_slug = vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    
    if request.user.is_authenticated:
        cartitem  =Cart.objects.filter(user=request.user)
    else:
        cartitem = None
    
    context={
        'vendor':vendor,
        'categories':categories,
        'cartitem':cartitem,
    }
    return render(request,'marketplace/vendor_detail.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        # if request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if food item exist or not
            try:
                fooditem=FoodItem.objects.get(id=food_id)
                print(fooditem)
                #Check if the user has already added same food to cart
                try:
                    checkcart = Cart.objects.get(user=request.user , fooditem=fooditem)
                    #Increase Cart Quantity
                    checkcart.quantity += 1
                    checkcart.save()
                    #return JsonResponse({'status': 'Success','message':'Increased Cart Quantity'})
                    #return JsonResponse({'status': 'Success','message':'Increased Cart Quantity','cart_counter': get_cart_counter(request),'qty':checkcart.quantity})
                    return JsonResponse({'status': 'Success','message':'Increased Cart Quantity','cart_counter': get_cart_counter(request),'qty':checkcart.quantity,'cart_amount':get_cart_amount(request)})

                except:
                    #if food is not added , we need to add food to the cart
                    checkcart = Cart.objects.create(user=request.user , fooditem=fooditem , quantity=1)
                    return JsonResponse({'status': 'Success','message':'Added food to cart','cart_counter': get_cart_counter(request),'qty':checkcart.quantity,'cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed','message':'This food doesnot exist'})

        else:
            #if ajax not there
            return JsonResponse({'status': 'Failed','message':'Invalid request'})
        #return JsonResponse({'status': 'success','message':'User is Logged in'}) 
    else:
        return JsonResponse({'status': 'login_required','message':'Please Login to continue'})

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        # if request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if food item exist or not
            try:
                fooditem=FoodItem.objects.get(id=food_id)
                print(fooditem)
                #Check if the user has already added same food to cart
                try:
                    checkcart = Cart.objects.get(user=request.user , fooditem=fooditem)
                    
                    if(checkcart.quantity>=1):
                    #Decrease Cart Quantity
                        checkcart.quantity -= 1
                        checkcart.save()
                    else:
                        checkcart.delete()
                        checkcart.quantity=0
                    
                    #return JsonResponse({'status': 'Success','message':'Increased Cart Quantity'})
                    return JsonResponse({'status': 'Success','message':'Decreased Cart Quantity','cart_counter': get_cart_counter(request),'qty':checkcart.quantity})

                except:
                    
                    return JsonResponse({'status': 'Failed','message':'You donot have the item in your cart'})
            except:
                return JsonResponse({'status': 'Failed','message':'This food doesnot exist'})

        else:
            #if ajax not there
            return JsonResponse({'status': 'Failed','message':'Invalid request'})
        #return JsonResponse({'status': 'success','message':'User is Logged in'}) 
    else:
        return JsonResponse({'status': 'login_required','message':'Please Login to continue'})
    
def cart(request):
    #print('test')
    cartitems = Cart.objects.filter(user=request.user)
    context={
        'cartitems':cartitems,
    }
    return render(request,'marketplace/cart.html',context)

def search(request):
    address=request.GET['address']
    #print('Address coming from home.html',address)
    latitude = request.GET['lat']
    longitude = request.GET['long']
    radius = request.GET['radius']
    keyword=request.GET['keyword']


    print(address,latitude,longitude,radius,keyword)
    
    #GET VENDOR IDS THAT HAS THE FOOD USER IS LOOKING FOR
    fetch_food_items = FoodItem.objects.filter(food_title__icontains=keyword,is_available=True).values_list('vendor',flat=True)
    #print(fetch_food_items)
    
    vendors = Vendor.objects.filter(Q(id__in=fetch_food_items)| Q(vendor_name__icontains=keyword , is_approved=True,user__is_active=True))
    print(vendors)
    #cat
    #vendors =Vendor.objects.filter(vendor_name__icontains=keyword , is_approved=True,user__is_active=True)
    print('Search',vendors)
    vendors_count=vendors.count()
    
    context={
        'vendors':vendors,
        'vendors_count':vendors_count,
        'fetch_food_item':fetch_food_items,
    }
    return render (request,'marketplace/listings.html',context)
