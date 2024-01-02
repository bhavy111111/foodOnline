from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
from django.contrib import auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify
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

            #SEND VERIFICATION EMAIL
            mail_subject = 'Please activate your account'
            email_template='accounts/emails/account_verification_email.html'

            send_verification_email(request,user,mail_subject,email_template)
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
            #==================vendor_slug for marketplace
            vendors_name=vendor_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendors_name)+'-'+str(user.id)
            #=====================================
            user_profile = UserProfile.objects.get(user=user)
        
            vendor.user_profile = user_profile
            vendor.save()
            #send verification mail
            mail_subject = 'Please activate your account'
            email_template='accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)

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

def activate(request,uidb64,token):
    #Activate the user by setting the is_active status to be true 

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User._default_manager.get(pk=uid)
        print(user)
    except(TypeError , ValueError , OverflowError, User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request , 'Congratulations! Your Account has been activated')
        return redirect('myaccount')
    else:
        messages.error(request,'Invalid Activation Link')
        return redirect('myaccount')

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

def reset_password_validate(request,uidb64 , token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User._default_manager.get(pk=uid)
        print(user)
    except(TypeError , ValueError , OverflowError, User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        
        messages.success(request , 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired!')
        return redirect('myaccount')


    return 

def forgot_password(request):

    if request.method=='POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

        #send reset password email 
            
            #send_password_reset_email(request,user)

            mail_subject = 'Reset your password'
            email_template='accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,'Password link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request,'Account doesnot exist')
            return redirect('forgot_password')
            
    return render(request,'accounts/forgot_password.html')

def reset_password(request):
    if request.method=='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.is_active=True
            user.save()
            messages.success(request,'Password Reset Successful')
            return redirect('login')

        else:
            messages.error(request,'Passwords do not match!')
            return redirect('reset_password')


    return render(request,'accounts/reset_password.html')

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
    # Using customer context processor , no need for these two lines
    #vendor = Vendor.objects.get(user=request.user)
   
    #print('Inside Vendor dashboard views',vendor)
    #context={
     #   'vendor':vendor,
    #}
    return render(request , 'accounts/vendordashboard.html')
