# Generated by Django 4.2.3 on 2023-09-20 06:37

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_customuser_age_customuser_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="wallet_balance",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0.00"),
                help_text="Wallet balance in user account.",
                max_digits=10,
            ),
        ),
    ]
