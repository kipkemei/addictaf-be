# Generated by Django 2.0.4 on 2018-05-21 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20180521_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='object_id',
            field=models.IntegerField(),
        ),
    ]