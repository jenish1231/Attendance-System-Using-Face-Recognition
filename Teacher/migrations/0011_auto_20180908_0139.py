# Generated by Django 2.1.1 on 2018-09-08 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0010_auto_20180907_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image_path',
            field=models.CharField(max_length=200),
        ),
    ]
