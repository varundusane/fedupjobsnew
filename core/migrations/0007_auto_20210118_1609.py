# Generated by Django 3.1.4 on 2021-01-18 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20201222_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workdetails',
            name='apply_job_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
