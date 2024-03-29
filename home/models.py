

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')
    slug = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Slider(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')
    url = models.URLField(max_length=500, blank=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media')
    description = models.TextField()
    rank = models.IntegerField()

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media')
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=200)
    subject = models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Information(models.Model):
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.address


STATUS = (('Active', 'Active'),('Inactive','Inactive'))
LABELS = (('new','new'),('hot','hot'),('sale','sale'),('','default'))


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = RichTextField()
    specification = RichTextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=100)
    labels = models.CharField(choices=LABELS, max_length=50)
    slug = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    star = models.IntegerField()
    comment = models.TextField()
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    username = models.CharField(max_length=200)
    quantity = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    checkout = models.BooleanField(default=False)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Wishlist(models.Model):
    username = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    items = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.username


orderstatuses = (('Pending', 'Pending'), ('Out for Shipping','Out for Shipping'), ('Completed','Completed'))


class Order(models.Model):
    username = models.CharField(max_length = 300, null= False)
    fname = models.CharField(max_length = 300, null= False)
    lname = models.CharField(max_length = 300, null= False)
    email = models.EmailField(max_length = 300, null= False)
    phone = models.CharField(max_length = 300, null= False)
    address = models.TextField(null= False)
    city = models.CharField(max_length = 300, null= False)
    state = models.CharField(max_length = 300, null= False)
    country = models.CharField(max_length = 300, null= False)
    pincode = models.CharField(max_length = 300, null= False)
    total_price  = models.FloatField(null = False)
    payment_mode = models.CharField(max_length = 300, null= False)
    payment_id = models.CharField(max_length = 300, null= True)
    status = models.CharField(max_length = 300, null= False, choices=orderstatuses, default= 'Pending')
    message = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now =True, auto_now_add=False)

    def str(self):
        return '{} - {}'.format(self.id)





