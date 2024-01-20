from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import Cart
from .context_processors import get_cart_counter,get_cart_amount
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance
from vendor.models import OpeningHour
from orders.forms import OrderForm
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
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
    print('Vendor_detail',vendor.id)
    
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    #############################################################
    hour_obj = OpeningHour.objects.filter(vendor=vendor.id).order_by('day','-from_hour')
    print('Test',hour_obj)
    ########################
    if request.user.is_authenticated:
        cartitem  =Cart.objects.filter(user=request.user)
    else:
        cartitem = None
    
    context={
        'vendor':vendor,
        'categories':categories,
        'cartitem':cartitem,
        'hour_obj':hour_obj,
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
    if not  'address' in  request.GET:
        return redirect('marketplace')
    else:
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
        #gdal configuration
        if(latitude and longitude and radius):
            #IN point long will be first
            pnt = GEOSGeometry('POINT(%s %s)'%(longitude,latitude))
            vendors = Vendor.objects.filter(Q(id__in=fetch_food_items)| Q(vendor_name__icontains=keyword , is_approved=True,user__is_active=True),
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance('user_profile__location',pnt)).order_by('distance')

        for v in vendors:
            v.kms = round(v.distance.km)

        #cat
        #vendors =Vendor.objects.filter(vendor_name__icontains=keyword , is_approved=True,user__is_active=True)
        print('Search',vendors)
        vendors_count=vendors.count()
        
        context={
            'vendors':vendors,
            'vendors_count':vendors_count,
            'fetch_food_item':fetch_food_items,
            'address':address,
        }
        return render (request,'marketplace/listings.html',context)
    
@login_required(login_url='login')
def checkout(request):
    user_profile = UserProfile.objects.get(user=request.user)
    default_dict={
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'phone':request.user.phone_number,
        'email':request.user.email,
        'address':user_profile.address,
        'country':user_profile.country,
        'state':user_profile.state,
        'city':user_profile.city,
        'pincode':user_profile.pincode

    }
    form=OrderForm(initial=default_dict)
    cartitems=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cartitems.count()
    if cart_count<=0:
        return redirect('marketplace')
    context={
        'form':form,
        'cartitems':cartitems,
    }
    return render(request,'marketplace/checkout.html',context)