# Generated by Django 4.2.3 on 2023-08-08 10:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_productcolor_productsize"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ProductColor",
        ),
        migrations.DeleteModel(
            name="ProductSize",
        ),
    ]