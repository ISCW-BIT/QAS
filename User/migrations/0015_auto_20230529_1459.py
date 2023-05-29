# Generated by Django 3.2.7 on 2023-05-29 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_auto_20230529_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ตำแหน่ง/ระดับชั้น'),
        ),
        migrations.AlterField(
            model_name='player',
            name='provide',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='จังหวัด'),
        ),
        migrations.AlterField(
            model_name='player',
            name='unit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='สังกัด/โรงเรียน'),
        ),
    ]
