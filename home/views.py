from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from django.contrib import messages

# Create your views here.


class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()


class HomeView(BaseView):
    def get(self, request):
        self.views
        self.views['subcategories'] = Subcategory.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['Brands'] = Brand.objects.all()
        self.views['new_products'] = Product.objects.filter(labels='new')
        self.views['hot_products'] = Product.objects.filter(labels='hot')

        return render(request, 'index.html', self.views)


def contact(request):
    views = {}
    views['information'] = Information.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        data = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
            )
        data.save()

    return render(request,'contact.html',views)


class ProductView(BaseView):
    def get(self, request, slug):
        self.views['product_detail'] = Product.objects.filter(slug=slug)
        self.views['product_review'] = ProductReview.objects.filter(slug=slug)
        subcat_id = Product.objects.get(slug = slug).subcategory_id
        products_id = Product.objects.get(slug = slug).id
        self.views['product_Image'] = ProductImage.objects.filter(product_id=products_id)
        self.views['related_product'] = Product.objects.filter(subcategory_id=subcat_id)

        return render(request,'product-detail.html', self.views)


def product_review(request, slug):
    if request.method == 'POST':
        username = request.user.username
        email = request.user.email
        star = request.POST['star']
        comment = request.POST['comment']
        data = ProductReview.objects.create(
            name=username,
            email=email,
            star=star,
            comment=comment,
            slug=slug,
        )
        data.save()

        messages.error(request, 'The review is Submited')

        return redirect(f'/product_detail/{slug}')






