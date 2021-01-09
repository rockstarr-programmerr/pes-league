# Generated by Django 3.1.5 on 2021-01-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0003_auto_20210109_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='away_team_score',
            field=models.PositiveIntegerField(verbose_name='bàn thắng đội khách'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_team_score',
            field=models.PositiveIntegerField(verbose_name='bàn thắng đội nhà'),
        ),
        migrations.AlterField(
            model_name='season',
            name='length',
            field=models.PositiveIntegerField(default=38, verbose_name='số vòng'),
        ),
    ]
