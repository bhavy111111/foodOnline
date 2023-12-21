from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
# Create your views here.

def registerUser(request):
    if request.method=='POST':
        print(request.POST)
        form=UserForm(request.POST)
        if form.is_valid():
            #assign the role
            #ready to save , watever data we have will go to user variable
            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #print(user)
            #user.role = User.CUSTOMER
            #user.set_password(password)
            #user.save()

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name = first_name , last_name=last_name,username=username , email = email,password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,"Your Account has been registered sucessfully!.")

            print('user has been created')
            return redirect('registerUser')
        else:
            print('Invalid form options')
            print(form.errors)
        #pass
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request , 'accounts/registerUser.html',context)

def registerVendor(request):
    if request.method == 'POST':
        #store the data and create the user
        form = UserForm(request.POST)
        #As we are passing license also which is in file format thats y request.files
        vendor_form=VendorForm(request.POST , request.FILES)
        print('VEDNOR FORM DETAIls',vendor_form)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            print('Cleaned first name ',first_name)
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name , last_name=last_name,username=username , email = email,password=password)
            user.role=user.VENDOR
            print('User details',user)
            user.save()
            vendor=vendor_form.save(commit=False)
            print('All vendor details',vendor)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
        
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your Vendor Account has been setup! ')
            return redirect('registerVendor')
        else:
            print(form.errors)
            print('Invalid form')


    else:

        form =UserForm()
        vendor_form = VendorForm()

    context={
        'form':form,
        'vendor_form':vendor_form,
    }

    return render(request,'accounts/registerVendor.html',context)