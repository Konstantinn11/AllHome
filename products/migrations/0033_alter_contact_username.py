# Generated by Django 4.2.7 on 2024-06-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_alter_zayavka_employer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='username',
            field=models.CharField(max_length=255, verbose_name='Имя пользователя'),
        ),
    ]
