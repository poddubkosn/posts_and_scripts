# Generated by Django 2.2.16 on 2021-10-01 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myscripts',
            name='image',
            field=models.ImageField(blank=True, help_text='Загрузите картинку', null=True, upload_to='blog/', verbose_name='Картинка'),
        ),
    ]
