from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
from django.contrib import auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

# Restrict the vendor from accessing customer endpoint

def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied
    
# Restrict the customer from accessing vendor endpoint
def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already registered!')
        return redirect('dashboard')
    elif request.method=='POST':
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
    if request.user.is_authenticated:
        messages.warning(request,'You are already registered as Vendor!')
        return redirect('myaccount')
    elif request.method == 'POST':
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

def login(request):
    #So that user cannot login again , it will redirected to dashboard page
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myaccount')
    
    #User have to login for first go
    elif request.method=='POST':
        #'email' is the name of html tag input
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)

        user = auth.authenticate(email=email,password=password)

        if user is not None :
            #login function of auth
            auth.login(request,user)
            messages.success(request,'You are now logged in!')
            return redirect('myaccount')
        else:
            messages.error(request,'Invalid Login Credentials!')
            return redirect('login')

    return render (request,'accounts/login.html')

def logout(request):

    auth.logout(request)
    messages.info(request , 'You are Logged out!')
    return redirect('login')


@login_required(login_url = 'login')
def myaccount(request):
    #request.user is a person who is logged in
    user = request.user
    print('myaccount user',user)
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerdashboard(request):
    return render(request , 'accounts/customerdashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render(request , 'accounts/vendordashboard.html')
