# Generated by Django 4.1.7 on 2023-04-10 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_cart_delete_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]