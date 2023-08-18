# Generated by Django 4.2.3 on 2023-08-18 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0015_order_total_quantity_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="total_price_shipping",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]