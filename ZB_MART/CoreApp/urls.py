from django.urls import path
from django.contrib import admin,auth
from django.conf import settings
from CoreApp import views
from .views import HomeView,ShopView,CategoryView,Cartview,add_to_cart,remove_from_cart,remove_single_item_from_cart
from django.contrib.auth import views as auth_views

app_name = 'CoreApp'

urlpatterns = [path('',HomeView.as_view(),name='home'),
               path('shop/', ShopView.as_view(), name='shop'),
               path('category/<slug>/', CategoryView.as_view(), name='category'),
               path('cart/', Cartview.as_view(), name='cart'),
                path('signup/', views.SignUp.as_view(), name='signup'),
                path('login/', auth_views.LoginView.as_view(), name='login'),
                path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
                path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
                path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
               ]