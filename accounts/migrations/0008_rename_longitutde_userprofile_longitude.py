# Generated by Django 5.0 on 2023-12-25 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_userprofile_address_line_1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='longitutde',
            new_name='longitude',
        ),
    ]
