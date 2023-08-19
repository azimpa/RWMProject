# Generated by Django 4.2.3 on 2023-08-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0024_alter_order_order_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="order_status",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("Order Placed", "Order Placed"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                ],
                default="Order Placed",
                max_length=20,
            ),
        ),
    ]