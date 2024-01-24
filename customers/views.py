from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User,UserProfile
from accounts.forms import UserProfileForm,UserInfoForm
from django.contrib import messages
from orders.models import Order,OrderedFood
# Create your views here.
@login_required(login_url='login')
def cprofile(request):

    profile = get_object_or_404(UserProfile,user=request.user)
    print(profile)

    #If and else is used at the time of updating Customer Profile
    if request.method=='POST':
        profile_form=UserProfileForm(request.POST , request.FILES , instance=profile)
        user_form=UserInfoForm(request.POST , request.FILES , instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile Updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        #print(profile_form)
        user_form=UserInfoForm()
        #print(user_form)

    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request ,'customers/cprofile.html',context)

def my_orders(request):
    order=Order.objects.filter(user=request.user,is_ordered=True)
    #print(order)

    context={
        'order':order,
    }
    return render(request,'customers/my_orders.html',context)

def order_details(request,order_number):
    try:
        order=Order.objects.get(order_number=order_number , is_ordered=True)
        print(order)
        #print(order)
        ordered_food=OrderedFood.objects.filter(order=order)
        print(ordered_food)
        context={
            'order':order,
            'ordered_food':ordered_food
        }

        return render(request,'customers/order_details.html',context)
    except:
        return redirect('customer')

   

    