# Generated by Django 4.2.7 on 2024-06-08 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_remove_act_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zayavka',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.employer', verbose_name='Исполнитель'),
        ),
    ]
