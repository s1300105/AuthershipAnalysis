# Generated by Django 5.0.4 on 2024-05-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedfile',
            name='keyword',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
