# Generated by Django 4.2.3 on 2023-08-29 09:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adm", "0025_alter_productcolor_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="admproducts",
            name="offer_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="admproducts",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]