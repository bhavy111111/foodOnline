from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages
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