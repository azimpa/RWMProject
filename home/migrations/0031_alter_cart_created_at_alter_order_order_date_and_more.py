# Generated by Django 4.2.3 on 2023-09-13 07:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0030_orderitem_return_reason_alter_cart_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 13, 12, 48, 8, 130830)
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 13, 12, 48, 8, 130830)
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("Order Placed", "Order Placed"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                    ("Return Requested", "Return Requested"),
                ],
                default="Order Placed",
                max_length=20,
            ),
        ),
    ]
