# Generated by Django 4.2.5 on 2023-09-27 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0003_remove_payment_user_remove_refund_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='being_delivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='received',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_granted',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_requested',
        ),
    ]