from django.urls import path
from django.contrib import admin,auth
from django.conf import settings
from CoreApp import views
from .views import HomeView,ItemDetailView,ShopView,CategoryView,Cartview
from django.contrib.auth import views as auth_views

urlpatterns = [path('',HomeView.as_view(),name='home'),
               path('shop/', ShopView.as_view(), name='shop'),
               path('category/<slug>/', CategoryView.as_view(), name='category'),
               path('cart/', Cartview.as_view(), name='cart'),
                path('signup/', views.SignUp.as_view(), name='signup'),
                path('login/', auth_views.LoginView.as_view(), name='login'),
                path('logout/', auth_views.LogoutView.as_view(), name='logout'),
               ]