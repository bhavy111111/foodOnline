# Generated by Django 5.0 on 2024-01-02 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_remove_vendor_vendor_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(blank=True),
        ),
    ]
