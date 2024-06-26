# Generated by Django 4.2.5 on 2024-03-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0008_photo_created_at_photo_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
