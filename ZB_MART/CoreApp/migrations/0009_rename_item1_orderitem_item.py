# Generated by Django 4.2.5 on 2023-10-03 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0008_rename_item_orderitem_item1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='item1',
            new_name='item',
        ),
    ]
