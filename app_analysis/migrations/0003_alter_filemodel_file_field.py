# Generated by Django 5.0.4 on 2024-05-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_analysis', '0002_selectedfile_keyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file_field',
            field=models.FileField(upload_to='Texts/uploaded'),
        ),
    ]
