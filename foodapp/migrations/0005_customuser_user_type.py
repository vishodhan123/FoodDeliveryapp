# Generated by Django 4.2.7 on 2023-11-17 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0004_restaurant_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('restaurant_owner', 'Restaurant Owner')], default='customer', max_length=25),
        ),
    ]
