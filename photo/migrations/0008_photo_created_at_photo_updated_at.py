# Generated by Django 4.2.5 on 2024-03-24 09:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0007_remove_photo_created_at_remove_photo_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
