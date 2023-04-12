from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('contact', contact, name='contact'),
    path('ProductView/<slug>', ProductView.as_view(), name='ProductView'),
    path('product_review/<slug>', product_review, name='product_review'),
    path('cart', CartView.as_view(), name='cart'),
    path('add_to_cart/<slug>',add_to_cart, name='add_to_cart'),
    path('reduce_quantity/<slug>', reduce_quantity, name='reduce_quantity'),
    path('delete_cart/<slug>', delete_cart, name='delete_cart'),
    path('count_cart/<slug>', count_cart, name='count_cart'),
    path('Shop', Shop.as_view(),name='Shop'),
    path('wishlist', WishlistView.as_view(), name='wishlist'),
    path('add_to_wishlist/<slug>', add_to_wishlist, name='add_to_wishlist'),
    path('delete_wish/<slug>', delete_wish, name='delete_wish'),
    path('count_wish/<slug>', count_wish, name='count_wish'),
    path('signup', signup, name='signup')


]
