# Generated by Django 4.2.3 on 2023-09-28 14:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0065_cart_cart_total_cart_total_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="cart_total",
        ),
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 28, 20, 18, 19, 404507)
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 28, 20, 18, 19, 409646)
            ),
        ),
    ]