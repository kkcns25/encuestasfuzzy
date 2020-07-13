# Generated by Django 2.1.7 on 2020-07-11 22:52

import base110.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base110', '0005_auto_20200709_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='static/csv', validators=[base110.models.Upload.validate_file_extension]),
        ),
    ]
