# Generated by Django 4.2.3 on 2023-08-18 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0014_alter_cartitem_product_alter_orderitem_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="total_quantity_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
