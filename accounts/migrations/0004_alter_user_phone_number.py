# Generated by Django 5.0 on 2023-12-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_cover_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]