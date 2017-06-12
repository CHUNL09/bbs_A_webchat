# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-23 13:29
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superbbs', '0003_auto_20160619_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='文章内容'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag_img',
            field=models.ImageField(upload_to='statics/pic', verbose_name='文章标题图片'),
        ),
    ]