# Generated by Django 5.0 on 2023-12-24 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]