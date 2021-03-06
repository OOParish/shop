# Generated by Django 3.2 on 2021-04-18 09:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_alter_order_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(help_text='Example: Pushkinska 13', max_length=250, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Zа-яА-Яё. ]+$')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(help_text='Example: Ivan, Dmytro, Vasya', max_length=50, validators=[django.core.validators.RegexValidator(message='Username must be Alphanumeric', regex='^([а-яА-Яё\\s]+|[a-zA-Z\\s]+)$')], verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.CharField(help_text='Example: 20501, 30512', max_length=5, validators=[django.core.validators.RegexValidator(regex='^(^[0-9]{5}(?:-[0-9]{4})?$|^$)')]),
        ),
    ]
