# Generated by Django 3.1 on 2020-09-01 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0032_auto_20200831_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='slug',
            field=models.SlugField(default='fdeladgelFjFolo', unique=True),
        ),
    ]
