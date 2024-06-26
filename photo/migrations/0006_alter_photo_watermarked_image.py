# Generated by Django 4.2.5 on 2024-03-24 08:28

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0005_rename_webp_image_photo_watermarked_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='watermarked_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='watermarked_image'),
        ),
    ]
