# Generated by Django 5.0.3 on 2024-04-01 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proforma', '0003_carmodel_is_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='carpart',
            name='is_enable',
            field=models.BooleanField(default=True, verbose_name='Habilitado'),
        ),
    ]
