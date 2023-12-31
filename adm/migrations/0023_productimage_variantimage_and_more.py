# Generated by Django 4.2.3 on 2023-08-21 15:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adm", "0022_alter_productvariant_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="product_images/")),
            ],
        ),
        migrations.CreateModel(
            name="VariantImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="variant_images/")),
            ],
        ),
        migrations.RemoveField(
            model_name="admproducts",
            name="product_image",
        ),
        migrations.RemoveField(
            model_name="productvariant",
            name="image",
        ),
        migrations.AddField(
            model_name="admproducts",
            name="images",
            field=models.ManyToManyField(blank=True, to="adm.productimage"),
        ),
        migrations.AddField(
            model_name="productvariant",
            name="images",
            field=models.ManyToManyField(blank=True, to="adm.variantimage"),
        ),
    ]
