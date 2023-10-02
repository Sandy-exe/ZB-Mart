from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.views.generic import TemplateView,ListView,DetailView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Item,Category,OrderItem,Order
from django.shortcuts import redirect, get_object_or_404
import time


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
class Cartview(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    print(order_item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(request.META.get('HTTP_REFERER'))
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item qty was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
    else:
        ordered_date = time.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url.endswith(reverse('CoreApp:cart')):
        return redirect("CoreApp:cart")
    # Redirect the user back to the previous page
    return redirect(previous_url)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Item was removed from your cart.")
            return redirect("CoreApp:cart")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("CoreApp:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("CoreApp:product", slug=slug)
    return redirect("CoreApp:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item qty was updated.")
            return redirect("CoreApp:cart")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("CoreApp:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("CoreApp:product", slug=slug)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")