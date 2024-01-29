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

    #Category CRUD
    path('menu-builder/category/add/',views.add_category,name='add_category'),
    path('menu-builder/category/edit/<int:pk>/',views.edit_category,name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/',views.delete_category,name='delete_category'),

    #Food CRUD

    path('menu-builder/food/add/',views.add_food,name='add_food'),
    path('menu-builder/food/edit/<int:pk>/',views.edit_food,name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/',views.delete_food , name="delete_food"),

    #Opening Hour CRUD
    path('opening_hours/',views.opening_hours , name="opening_hours"),
    path('opening_hours/add/',views.opening_hours_add , name="opening_hours_add"),

    #Decrease or remove Hours

    path('opening_hours/remove/<int:pk>/',views.remove_opening_hour,name="remove_opening_hour"),

    path('order_detail/<int:order_number>/',views.order_detail,name="order_detail"),







]