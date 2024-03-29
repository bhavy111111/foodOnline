from django.shortcuts import render,get_object_or_404,redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor,OpeningHour
from django.contrib import messages
from menu.models import Category,FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from menu.forms import FoodItemForm
from django.http import HttpResponse
from .forms import OpeningForm
from django.db import IntegrityError
from django.http import JsonResponse
from orders.models import Order,OrderedFood

# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

def vprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)
    
    if request.method=='POST':
        profile_form=UserProfileForm(request.POST,request.FILES , instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES , instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings got Updated')

            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        vendor_form=VendorForm(instance=vendor)

    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor
    }
    return render(request , 'vendor/vprofile.html',context)

@login_required(login_url='login')
def menu_builder(request):

    vendor = get_vendor(request)
    #print('Logged In',vendor)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context={
        'vendor':vendor,
        'categories': categories,
    }
    return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='login')
def food_item_by_category(request,pk=None):
    vendor= get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(vendor=vendor,category=category)
    print(fooditems)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    return render(request,'vendor/food_item_by_category.html',context)

@login_required(login_url='login')
def add_category(request):
    if request.method=='POST':
        form = CategoryForm(request.POST)
        print('Add Category Form',form)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor=get_vendor(request)
            print('Inside',category)
            #category.save() #here id will be generated
            #print('save',category.save())

            category.save()# cat id will be generated
           
            category.slug = slugify(category_name)+'-'+str(category.id)
            #category name is chicken - Slug will be chicken-{category id} as in chicken-15
            category.save()
            messages.success(request,'Category added successfully')
            return redirect ('menu_builder')
        else:
            #Duplicacy of category will give this error
            print(form.errors)
    else:
        form = CategoryForm()
    context={
        'form':form,
    }
    return render(request,'vendor/add_category.html',context)
@login_required(login_url='login')
def edit_category(request,pk=None):
    #pk --> menu_builder.html cat.id
    category = get_object_or_404(Category , pk=pk)

    if request.method=='POST':
        form = CategoryForm(request.POST,instance=category)
        print('Add Category Form',form)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor=get_vendor(request)
            ########
            #print('Inside category.vendor',vendor)
            ########
            category.slug = slugify(category_name)
            print('form end',form)
            form.save()
            messages.success(request,'Category Update successfully')
            return redirect ('menu_builder')
        else:
            #Duplicacy of category will give this error
            print(form.errors)
    else:
        form =CategoryForm(instance=category)
    context={
        'form':form,
        'category':category
                }
    return render(request , 'vendor/edit_category.html',context)

def delete_category(request,pk=None):
    category = get_object_or_404(Category , pk=pk)
    print(category)
    category.delete()
    messages.success(request , 'Category updated Successfully!')
    return redirect ('menu_builder')


def add_food(request):
    if request.method=='POST':
        form = FoodItemForm(request.POST,request.FILES)
        print('Add Food Form',form)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor=get_vendor(request)
            ########
            #print('Inside category.vendor',vendor)
            ########
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request,'Food added successfully')
            return redirect ('food_item_by_category',food.category.id)
        else:
            #Duplicacy of category will give this error
            print(form.errors)
    else:
        form = FoodItemForm()
    context={
        'form':form,
    }
    return render(request,'vendor/add_food.html',context)

def edit_food(request,pk=None):

    #pk --> menu_builder.html cat.id
    food = get_object_or_404(FoodItem , pk=pk)

    if request.method=='POST':
        form = FoodItemForm(request.POST,instance=food)
        print('Add Food Form',form)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor=get_vendor(request)
            ########
            #print('Inside category.vendor',vendor)
            ########
            food.slug = slugify(foodtitle)
            print('form end',form)
            form.save()
            messages.success(request,'Food  Update successfully')
            return redirect ('food_item_by_category',food.category.id)
        else:
            #Duplicacy of category will give this error
            print(form.errors)
    else:
        form =FoodItemForm(instance=food)
    context={
        'form':form,
        'food':food
    }
    return render(request , 'vendor/edit_food.html',context)

def delete_food(request,pk=None):
    food = get_object_or_404(FoodItem ,pk=pk)
    print(food)
    food.delete()
    messages.success(request, 'Food Item has been deleted ')
    return redirect('food_item_by_category',food.category.id)

def opening_hours(request):
    opening_hours=OpeningHour.objects.filter(vendor=get_vendor(request))
    print(opening_hours)
    form=OpeningForm()
    context={
        'form': form,
        'opening_hours':opening_hours,

    }
    return render(request,'vendor/opening_hours.html',context)

def opening_hours_add(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            day=request.POST.get('day')
            from_hour=request.POST.get('from_hour')
            to_hour=request.POST.get('to_hour')
            is_closed=request.POST.get('is_closed')

            try:
                #return hour id or day 6- Sunday
                hour=OpeningHour.objects.create(vendor=get_vendor(request),day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                print('Inside creating',hour)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    print('Inside',day)
                    if day.is_closed:
                        response={'status':'success','id':hour.id,'day':day.get_day_display(),'is_closed':'Closed'}
                    else:
                        response={'status':'success','id':hour.id,'day':day.get_day_display(),'from_hour':hour.from_hour,'to_hour':hour.to_hour}

                #response={'status':'Success'}
                return JsonResponse(response)

            except IntegrityError as e:
                response={'status':'Failed','message':from_hour+'-'+to_hour+'Already exist'}
                return JsonResponse(response)            
            print(day,from_hour,to_hour,is_closed)

        else:
            return HttpResponse('Invalid data')

def remove_opening_hour(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour=get_object_or_404(OpeningHour,pk=pk)
            print(hour)
            hour.delete()
            print('Selected Hour has been deleted')
            return JsonResponse({'status':'success','id':pk})
    #return JsonResponse(response)

def order_detail(request,order_number=None):
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        print(order)
        ordered_food=OrderedFood.objects.filter(order=order,fooditem__vendor=get_vendor(request))
        print('ORDERED FOOD',ordered_food)

        context={
            'order':order,
            'ordered_food':ordered_food,
        }
    except:
        return redirect('vendor')
    return render(request,'vendor/order_detail.html',context)





    


