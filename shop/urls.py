from django.urls import path,include
from .import views
from  .views import OrderSummaryView,SearchView



urlpatterns = [
    path('home/', views.store, name='home'),
     path('product/', views.product, name='product'),
    path('product/<slug>', views.store_detail, name='store-detail'),
    path('cart/<slug>', views.add_to_cart, name='cart'),
    path('remove/<slug>', views.remove_item_cart, name='remove_item'),
     path('remove-single/<slug>', views.remove_single_item_cart, name='remove_single_item'),
    path('order-summary/',OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', SearchView.as_view(), name='search' ),
    path('process_order/',views.process_order, name='process' )
]