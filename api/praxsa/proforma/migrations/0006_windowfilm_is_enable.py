# Generated by Django 5.0.3 on 2024-04-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proforma', '0005_carmodelpart_is_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='windowfilm',
            name='is_enable',
            field=models.BooleanField(default=True, verbose_name='Habilitado'),
        ),
    ]
