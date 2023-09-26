from django.shortcuts import render

from django.views.generic import TemplateView,ListView,DetailView, View
# Create your views here.
from .models import Item
class HomeView(ListView):
    template_name = "index.html"
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"