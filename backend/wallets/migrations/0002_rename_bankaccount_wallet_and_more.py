# Generated by Django 5.2.4 on 2025-07-26 14:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="BankAccount",
            new_name="Wallet",
        ),
        migrations.RenameField(
            model_name="operation",
            old_name="bank_account",
            new_name="wallet",
        ),
    ]
