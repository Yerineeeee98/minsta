# Generated by Django 5.1.7 on 2025-04-02 07:59

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=-1, scale=None, size=[500, 500], upload_to='image/%Y/%m'),
        ),
    ]
