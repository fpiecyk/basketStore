# Generated by Django 4.2.7 on 2023-12-14 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0007_alter_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
    ]
