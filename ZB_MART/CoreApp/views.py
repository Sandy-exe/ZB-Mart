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
from datetime import datetime


class HomeView(ListView):
    def get(self, *args, **kwargs):
        item = Item.objects.filter(is_active=True)
        context={}
        context['object_list'] = item
        try:
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context['object'] = order
                return render(self.request, 'index.html', context)
            else:
                context = {'object_list': Item.objects.filter(is_active=True)}
                return render(self.request, 'index.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'index.html',context)

class ShopView(ListView):
    def get(self, *args, **kwargs):
        item = Item.objects.filter(is_active=True)
        context={}
        context['object_list'] = item
        try:
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context['object'] = order
                return render(self.request, 'shop.html', context)
            else:
                context = {'object_list': Item.objects.filter(is_active=True)}
                return render(self.request, 'shop.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'shop.html',context)
    model = Item
    paginate_by = 6

class CategoryView(View):
     def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug']) 
        item = Item.objects.filter(category=category, is_active=True)
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image,
        }
        try:
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context['object'] = order
            return render(self.request, 'category.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'category.html',context)

class Cartview(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context = { 'object': order }
                return render(self.request, 'cart.html', context)
            else:
                return render(self.request, 'cart.html')
        except ObjectDoesNotExist:
            render(self.request, 'cart.html')


# @login_required
def add_to_cart(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        if created==True:
            order_item = OrderItem.objects.get(item=item,user=request.user,ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item_in_cart = order.items.filter(item__slug=item.slug)[0]
                order_item_in_cart.quantity += 1
                order_item_in_cart.save()
                messages.info(request, "Item qty was updated.")
            else:
                order.items.add(order_item)
                messages.info(request, "Selected Item was added to your cart.")
        else:
            ordered_date = datetime.now()
            order = Order.objects.create(id_order=1,
                user=request.user, ordered_date=ordered_date)
            messages.info(request, "New Item was added to your cart.")
            
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url.endswith(reverse('CoreApp:cart')):
            return redirect("CoreApp:cart")
        # Redirect the user back to the previous page
        return redirect(previous_url)
    else:
        return redirect('CoreApp:login')

# @login_required
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
            )
            order_item.delete()
            messages.info(request, "Item was removed from your cart.")
            return redirect("CoreApp:cart")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("CoreApp:cart", slug=slug)
    else:
        return redirect("CoreApp:cart", slug=slug)


# @login_required
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
            return redirect("CoreApp:cart", slug=slug)
    else:
        return redirect("CoreApp:cart", slug=slug)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('CoreApp:home')
    template_name = 'registration/signup.html'

