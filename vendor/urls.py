from django.urls import path
from django.urls import include
from . import views
from accounts import views as AccountViews
urlpatterns = [
    #127.0.0.1:8000/accounts/vendor
    path('', AccountViews.vendordashboard,name='vendor'),

    path('profile/',views.vprofile,name='vprofile'),
]