# Generated by Django 3.2.7 on 2021-09-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examplegdprmodel',
            name='first_name',
            field=models.CharField(db_column='pa_first_name', max_length=255, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='examplegdprmodel',
            name='last_name',
            field=models.CharField(db_column='pa_last_name', max_length=255, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='examplegdprmodel',
            name='phone_number',
            field=models.CharField(blank=True, db_column='pa_phone_number', default='', max_length=255, verbose_name='Phone number'),
        ),
        migrations.AlterModelTable(
            name='examplegdprmodel',
            table='pa_example_examplegdprmodel',
        ),
    ]
