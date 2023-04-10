from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('contact', contact, name='contact'),
    path('ProductView/<slug>', ProductView.as_view(), name='ProductView'),
    path('product_review/<slug>', product_review, name='product_review')
]
