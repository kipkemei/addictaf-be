# Generated by Django 2.0.4 on 2018-05-21 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20180513_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.CharField(default='INSTAGRAM', max_length=25),
        ),
    ]