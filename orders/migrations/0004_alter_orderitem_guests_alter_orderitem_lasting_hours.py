# Generated by Django 4.2 on 2024-10-04 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orderitem_lasting_hr_orderitem_lasting_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='guests',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='lasting_hours',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
