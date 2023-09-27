from django.shortcuts import render

from django.views.generic import TemplateView,ListView,DetailView, View
# Create your views here.
from .models import Item,Category
class HomeView(ListView):
    template_name = "index.html"
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"

class ShopView(ListView):
    model = Item
    paginate_by = 6
    template_name = "shop.html"

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(category=category, is_active=True)
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "category.html", context)
class Cartview(ListView):
    model = Item
    template_name = "cart.html"