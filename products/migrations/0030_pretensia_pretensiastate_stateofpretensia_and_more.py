# Generated by Django 4.2.7 on 2024-05-23 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_act_image_dogovor_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pretensia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30, verbose_name='Номер претензии')),
                ('date_document', models.DateField(verbose_name='Дата документа')),
                ('image', models.ImageField(blank=True, upload_to='documents/', verbose_name='Претензия (.jpeg, .png)')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.customer', verbose_name='Заказчик')),
                ('dogovor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.dogovor', verbose_name='Номер договора')),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.employer', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': ('Претензия',),
                'verbose_name_plural': 'Претензии',
            },
        ),
        migrations.CreateModel(
            name='PretensiaState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Статус претензии')),
            ],
            options={
                'verbose_name': 'Статус претензии',
                'verbose_name_plural': 'Статусы претензии',
            },
        ),
        migrations.CreateModel(
            name='StateofPretensia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата статуса')),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.employer', verbose_name='Сотрудник')),
                ('pretensia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stateopretensias', to='products.pretensia', verbose_name='Претензия')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stateopretensias', to='products.pretensiastate', verbose_name='Статус претензия')),
            ],
            options={
                'verbose_name': 'Статус в претензии',
                'verbose_name_plural': 'Статусы в претензии',
            },
        ),
        migrations.CreateModel(
            name='Position_Pretensia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolichestvo', models.CharField(max_length=30, verbose_name='Количество услуг')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.position_price', verbose_name='Позиция прайс-листа')),
                ('pretensia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.pretensia', verbose_name='Номер акта')),
            ],
            options={
                'verbose_name': ('Позиция претензии',),
                'verbose_name_plural': 'Позиции претензии',
            },
        ),
    ]