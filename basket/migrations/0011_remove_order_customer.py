# Generated by Django 4.2.7 on 2023-12-14 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0010_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
    ]
