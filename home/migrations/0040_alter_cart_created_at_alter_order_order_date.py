# Generated by Django 4.2.3 on 2023-09-20 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0039_orderitem_refund_added_to_wallet_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 20, 17, 50, 34, 197733)
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 20, 17, 50, 34, 197733)
            ),
        ),
    ]
