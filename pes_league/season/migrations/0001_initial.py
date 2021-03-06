# Generated by Django 3.1.5 on 2021-01-09 07:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Tên')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('length', models.IntegerField(default=38, verbose_name='Số vòng')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Tên')),
                ('manager', models.CharField(max_length=255, verbose_name='Huấn luyện viên')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team_score', models.IntegerField(verbose_name='Số bàn đội nhà')),
                ('away_team_score', models.IntegerField(verbose_name='Số bàn đội khách')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Ngày thi đấu')),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='season.team', verbose_name='Đội khách')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='season.team', verbose_name='Đội nhà')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='season.season', verbose_name='Mùa giải')),
            ],
        ),
    ]
