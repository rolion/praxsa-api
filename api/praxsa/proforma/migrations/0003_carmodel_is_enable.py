# Generated by Django 5.0.3 on 2024-04-01 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proforma', '0002_carbrand_is_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='is_enable',
            field=models.BooleanField(default=True, verbose_name='Habilitado'),
        ),
    ]