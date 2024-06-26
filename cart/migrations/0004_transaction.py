# Generated by Django 4.2.5 on 2024-03-14 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_remove_cart_session_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                (
                    "payment_method",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("created_date", models.DateTimeField(blank=True, null=True)),
                (
                    "confirmation_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "payment_status_description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("message", models.TextField(blank=True, null=True)),
                (
                    "payment_account",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("call_back_url", models.URLField(blank=True, null=True)),
                ("status_code", models.IntegerField(blank=True, null=True)),
                (
                    "merchant_reference",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "payment_status_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("currency", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "cart",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transaction",
                        to="cart.cart",
                    ),
                ),
            ],
        ),
    ]
