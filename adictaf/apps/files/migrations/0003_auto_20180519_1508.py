# Generated by Django 2.0.4 on 2018-05-19 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='upload',
            field=models.FileField(upload_to='files/documents'),
        ),
    ]