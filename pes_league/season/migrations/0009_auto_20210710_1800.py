# Generated by Django 3.1.5 on 2021-07-10 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0008_auto_20210626_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='away_team_score',
            field=models.PositiveSmallIntegerField(verbose_name='bàn thắng đội khách'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_team_score',
            field=models.PositiveSmallIntegerField(verbose_name='bàn thắng đội nhà'),
        ),
        migrations.AlterField(
            model_name='game',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='season.season', verbose_name='mùa giải'),
        ),
        migrations.AlterField(
            model_name='season',
            name='length',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='số vòng'),
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(verbose_name='vòng số')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='season.season', verbose_name='vòng đấu')),
            ],
            options={
                'verbose_name': 'vòng đấu',
                'verbose_name_plural': 'vòng đấu',
                'ordering': ['number'],
            },
        ),
        migrations.AddField(
            model_name='game',
            name='round',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='season.round', verbose_name='vòng đấu'),
        ),
    ]
