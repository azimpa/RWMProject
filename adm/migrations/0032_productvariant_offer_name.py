# Generated by Django 4.2.3 on 2023-09-22 08:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adm", "0031_remove_productvariant_popularity"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="offer_name",
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
