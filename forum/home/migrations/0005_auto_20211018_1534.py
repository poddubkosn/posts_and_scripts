# Generated by Django 2.2.16 on 2021-10-18 05:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20211018_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Поле для ввода поста', max_length=12000, null=True, verbose_name='Пост'),
        ),
    ]
