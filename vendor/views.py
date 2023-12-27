from django.shortcuts import render,get_object_or_404,redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from menu.models import Category,FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='login')
def menu_builder(request):

    vendor = Vendor.objects.get(user=request.user)
    print('Logged In',vendor)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
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

def add_category(request):
    vendor= Vendor.objects.get(user=request.user)

    print(vendor)
    if request.method=='POST':
        form = CategoryForm(request.POST)
        print('Add Category Form',form)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor=vendor
            ########
            print('Inside category.vendor',vendor)
            ########
            category.slug = slugify(category_name)
            form.save()
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

def edit_category(request,pk=None):
    vendor= Vendor.objects.get(user=request.user)

    #pk --> menu_builder.html cat.id
    category = get_object_or_404(Category , pk=pk)

    if request.method=='POST':
        form = CategoryForm(request.POST,instance=category)
        print('Add Category Form',form)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor=vendor
            ########
            print('Inside category.vendor',vendor)
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

