# Generated by Django 4.2.3 on 2023-10-03 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0086_alter_cart_created_at_alter_order_order_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 10, 3, 15, 22, 32, 624673)
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 10, 3, 15, 22, 32, 632682)
            ),
        ),
    ]
