from django.urls import path
from django.urls import include
from . import views
from accounts import views as AccountViews
urlpatterns = [
    #127.0.0.1:8000/accounts/vendor
    path('', AccountViews.vendordashboard,name='vendor'),

    path('profile/',views.vprofile,name='vprofile'),
    path('menu-builder/',views.menu_builder,name='menu_builder'),
    path('menu-builder/category/<int:pk>/',views.food_item_by_category,name='food_item_by_category'),


]