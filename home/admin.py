from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)
admin.site.register(Contact)
admin.site.register(Information)
# admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
# admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "subcategory", "labels")
    list_filter = ("category", "labels", "status")
    search_field = ("name", "description")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("username","slug","quantity","total","checkout")
    list_filter = ("checkout","date")
    search_fields = ("username",)