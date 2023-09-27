from django.urls import path 
from .views import HomeView,ItemDetailView,ShopView,CategoryView,Cartview
urlpatterns = [path('',HomeView.as_view(),name='home'),
               path('shop/', ShopView.as_view(), name='shop'),
               path('category/<slug>/', CategoryView.as_view(), name='category'),
               path('cart/', Cartview.as_view(), name='cart'),
               ]