# Generated by Django 5.0 on 2024-01-29 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_tax_date_order_tax_data'),
        ('vendor', '0012_alter_openinghour_to_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.ManyToManyField(blank=True, to='vendor.vendor'),
        ),
    ]
