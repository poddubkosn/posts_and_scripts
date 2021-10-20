# Generated by Django 2.2.16 on 2021-10-19 06:44

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_myscripts_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Поле для ввода комментария', verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='myscripts',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Поле для ввода техта скрипта', verbose_name='техт скрипта'),
        ),
    ]