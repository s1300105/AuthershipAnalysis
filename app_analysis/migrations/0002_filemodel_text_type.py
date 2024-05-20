# Generated by Django 5.0.6 on 2024-05-16 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='text_type',
            field=models.CharField(blank=True, choices=[('Q', 'Questioned'), ('K', 'Known'), ('R', 'Reference')], max_length=10),
        ),
    ]
