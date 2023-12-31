# Generated by Django 4.2.3 on 2023-09-24 06:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("adm", "0038_remove_productvariant_discount_and_more"),
        ("home", "0051_alter_cart_created_at_alter_order_order_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="adm.coupon",
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 24, 11, 46, 16, 502673)
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 24, 11, 46, 16, 502673)
            ),
        ),
    ]
