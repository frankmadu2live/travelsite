# Generated by Django 5.0.6 on 2024-05-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjob', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='job_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]