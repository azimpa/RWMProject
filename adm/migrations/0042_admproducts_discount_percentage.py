# Generated by Django 4.2.3 on 2023-09-25 06:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adm", "0041_admproducts_offer_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="admproducts",
            name="discount_percentage",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]