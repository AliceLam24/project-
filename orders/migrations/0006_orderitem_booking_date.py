# Generated by Django 4.2 on 2024-10-04 13:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderitem_related_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='booking_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
