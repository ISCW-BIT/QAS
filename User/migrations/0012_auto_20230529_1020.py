# Generated by Django 3.2.7 on 2023-05-29 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_auto_20220609_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='คะแนนรวม'),
        ),
        migrations.AlterField(
            model_name='player',
            name='time',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='เวลารวม'),
        ),
    ]
