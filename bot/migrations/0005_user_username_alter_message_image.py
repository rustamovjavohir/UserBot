# Generated by Django 4.1.2 on 2022-10-15 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_message_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='message'),
        ),
    ]
