# Generated by Django 4.2.3 on 2023-08-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adm", "0027_admcategories_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="productcolor",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="productsize",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
