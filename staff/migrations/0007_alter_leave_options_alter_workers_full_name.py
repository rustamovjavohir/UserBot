# Generated by Django 4.0.2 on 2022-08-15 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_alter_total_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leave',
            options={'verbose_name': 'Выплаты', 'verbose_name_plural': 'Выплаты'},
        ),
        migrations.AlterField(
            model_name='workers',
            name='full_name',
            field=models.CharField(max_length=70, unique=True, verbose_name='Ф.И.О'),
        ),
    ]
