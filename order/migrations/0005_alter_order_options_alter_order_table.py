# Generated by Django 5.1.7 on 2025-04-12 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_orderitem_booked_date_alter_orderitem_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelTable(
            name='order',
            table='Order',
        ),
    ]
