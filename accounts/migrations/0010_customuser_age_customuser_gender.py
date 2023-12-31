# Generated by Django 4.2.3 on 2023-08-10 05:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0009_alter_customuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="age",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customuser",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                default=0,
                max_length=10,
            ),
            preserve_default=False,
        ),
    ]
