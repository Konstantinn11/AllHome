# Generated by Django 4.2.7 on 2024-05-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_customuser_chekbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='chekbox',
        ),
        migrations.AddField(
            model_name='customer',
            name='soglasie',
            field=models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных'),
        ),
    ]
