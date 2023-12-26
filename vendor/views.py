from django.shortcuts import render,get_object_or_404,redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from menu.models import Category,FoodItem
# Create your views here.

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

def menu_builder(request):

    vendor = Vendor.objects.get(user=request.user)
    print('Logged In',vendor)
    categories = Category.objects.filter(vendor=vendor)
    context={
        'vendor':vendor,
        'categories': categories,
    }
    return render(request,'vendor/menu_builder.html',context)

def food_item_by_category(request,pk=None):
    vendor= Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(vendor=vendor,category=category)
    print(fooditems)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    return render(request,'vendor/food_item_by_category.html',context)

