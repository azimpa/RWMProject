# Generated by Django 4.2.3 on 2023-08-18 13:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0016_order_total_price_shipping"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="total_quantity_price",
        ),
    ]
