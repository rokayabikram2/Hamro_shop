from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['sale_products'] = Product.objects.filter(labels='sale')
    views['information'] = Information.objects.all()


class HomeView(BaseView):
    def get(self, request):
        self.views
        self.views['cart_counts '] = count_cart(request)
        self.views['wish_counts'] = count_wish(request)
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
        self.views['cart_counts '] = count_cart(request)
        self.views['wish_counts'] = count_wish(request)
        self.views['product_detail'] = Product.objects.filter(slug=slug)
        self.views['product_review'] = ProductReview.objects.filter(slug=slug)
        subcat_id = Product.objects.get(slug=slug).subcategory_id
        products_id = Product.objects.get(slug=slug).id
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

        messages.error(request, 'The review is Submited.')

        return redirect(f'/product_detail/{slug}')


class Shop(BaseView):
    def get(self,request):
        self.views['cart_counts']= count_cart(request)
        query = request.GET.get("query")
        if query == "":
            return redirect('/')
        else:
            self.views['search_products'] = Product.objects.filter(description__icontains=query)

        return render(request,'shop.html',self.views)


class CartView(BaseView):
    def get(self,request):
        self.views['cart_counts'] = count_cart(request)
        self.views['wish_counts'] = count_wish(request)
        username = request.user.username
        self.views['cart_view'] = Cart.objects.filter(username =username)

        s = 0
        for i in self.views['cart_view']:
            s = s + i.total
        self.views['sub_total'] = s
        self.views['delivery_charge'] = 100
        self.views['grand_total'] = s + 100
        return render(request, 'cart.html', self.views)


def add_to_cart(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Cart.objects.filter(slug=slug,checkout=False,username=username).exists():
            quantity = Cart.objects.get(slug=slug,checkout=False, username=username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            quantity = quantity + 1
            if discounted_price > 0:
                total = discounted_price * quantity

            else:
                total = price * quantity
            Cart.objects.filter(slug=slug, checkout=False, username=username).update(total=total, quantity=quantity)

        else:
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if discounted_price > 0:
                total = discounted_price
            else:
                total = price
            data = Cart.objects.create(
                username=username,
                slug=slug,
                total=total,
                quantity=1,
                items=Product.objects.get(slug=slug)

            )
            data.save()

    else:
        return redirect('/')

    return redirect('/cart')


def reduce_quantity(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Cart.objects.filter(slug=slug, checkout=False, username=username).exists():
            quantity = Cart.objects.get(slug=slug,checkout=False,username=username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if quantity > 1:
                quantity = quantity - 1
                if discounted_price > 0:
                    total = discounted_price * quantity

                else:
                    total = price * quantity
                Cart.objects.filter(slug=slug, checkout=False, username=username).update(total=total, quantity=quantity)

            else:
                messages.error(request,'The quantity is already  1.')

    return redirect('/cart')


def delete_cart(request,slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Cart.objects.filter(slug=slug, checkout=False,username=username).exists():
            Cart.objects.filter(slug=slug, checkout=False, username=username).delete()

    return redirect('/cart')


def count_cart(request):
    username = request.user.username
    cart_count = Cart.objects.filter(checkout =False,username=username).count()
    return cart_count


class WishlistView(BaseView):
    def get(self,request):
        self.views['cart_counts'] = count_cart(request)
        self.views['wish_counts'] = count_wish(request)
        username= request.user.username
        self.views['wish_view'] = Wishlist.objects.filter(username=username)

        return render(request, 'wishlist.html', self.views)


def add_to_wishlist(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Wishlist.objects.filter(slug=slug, username=username).exists():
            messages.error(request, "The product is already exists")

        else:
            data = Wishlist.objects.create(
                username=username,
                slug=slug,
                items=Product.objects.get(slug=slug)

            )
            data.save()
            messages.success(request,"Product successfully added to wishlist")

    return redirect('/')


def delete_wish(request, slug):
    username = request.user.username
    if Product.objects.filter(slug=slug).exists():
        if Wishlist.objects.filter(slug=slug, username=username).exists():
            Wishlist.objects.filter(slug=slug, username=username).delete()
    return redirect('/wishlist')


def count_wish(request):
    username = request.user.username
    wish_count = Wishlist.objects.filter(username=username).count()
    return wish_count


def signup(request):
    if request.method == "POST":
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request,'The username is already taken.')
                return redirect('/signup')

            elif User.objects.filter(email=email).exists():
                messages.error(request,'The email is already used.')
                return redirect('/signup')

            else:
                data = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password
                )
                data.save()

        else:
            messages.error(request, 'The password does not match.')
    return render(request, 'signup.html')


class CheckoutView(BaseView):
    def get(self, request):
        self.views["wish_counts"] = count_wish(request)
        self.views["cart_counts"] = count_cart(request)
        username = request.user.username
        self.views['orders'] = Cart.objects.filter(username=username)
        s = 0
        for i in self.views["orders"]:
            s = s + i.total
        self.views["sub_total"] = s
        self.views['delivery_charge'] = 100
        self.views['grand_total'] = s+100

        return render(request, 'checkout.html', self.views)

    def placeorder(request):
        if request.method == 'POST':
            neworder = Order()
            neworder.fname = request.POST['fname']
            neworder.lname = request.POST['lname']
            neworder.email = request.POST['email']
            neworder.phone = request.POST['phone']
            neworder.address = request.POST['address']
            neworder.city = request.POST['city']
            neworder.state = request.POST['state']
            neworder.country = request.POST['country']
            neworder.pincode = request.POST['pincode']

            neworder.payment_mode = request.POST['payment_mode']

            Cart.objects.filter(username = request.user.username).delete()
            messages.success(request, "Your order has been placed successfully")
        return redirect('/')
