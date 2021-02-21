from django.shortcuts import render,get_object_or_404,redirect
from .models import Item,Order,OrderItem,Shipping
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json


def store(request):
    items = Item.objects.all()[0:12]
    return render(request, 'shop/store.html', {'items': items})
 


def store_detail(request, slug):
    object = get_object_or_404(Item, slug=slug)
    return render(request, 'shop/store_detail.html', {'object': object})


    
def product(request):
    object = Item.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(object, 8)
    try:
        items = paginator.page(page)
    except PageNoteAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, 'shop/product.html', {'object': items})
 






class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, complete=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        customer=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(customer=request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if orderitem is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('order-summary')
    else:
        date_added = timezone.now()
        order = Order.objects.create(customer=request.user, date_added=date_added)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('order-summary')







def checkout(request):
    order = Order.objects.get(customer=request.user, complete=False)
    context = {
                'object': order
            }
    return render(request, 'shop/checkout.html', context)
    












class SearchView(ListView):
    model = Item
    template_name = 'shop/product.html'
    context_object_name = 'object'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
        return object_list







@login_required
def remove_item_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(customer= request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug= item.slug).exists():
            order_item = OrderItem.objects.filter(customer=request.user, ordered=False, item= item)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("order-summary")
    else:
        messages.info(request, "you tdo not have an order.")
        return redirect("store-detail", slug=slug)






@login_required
def remove_single_item_cart(request,  slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(customer=request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if item exist in cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(customer=request.user, ordered=False,item=item)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, f"Cart has been updated")
            return redirect('order-summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("store-detail", slug=slug)
    else:
        messages.info(request, "you do not have a actice order")
        return redirect("store-detail", slug=slug)









def process_order(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,complete=False ) 
    total = float(data['form']['total'])

    if total == order.get_total:
        order.complete = True
    order.save()
    print(data)
    if order.shipping != False:
        Shipping.objects.create(
            customer=customer,
            address=data['shipping']['address'],
		    city=data['shipping']['city'],
		    state=data['shipping']['state'],
		    zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment submitted', safe= False)

















