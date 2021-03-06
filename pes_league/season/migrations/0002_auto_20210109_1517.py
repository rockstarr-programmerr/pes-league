# Generated by Django 3.1.5 on 2021-01-09 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='slug',
            field=models.SlugField(default='', max_length=255, unique=True, verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Tên'),
        ),
    ]
