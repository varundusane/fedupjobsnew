# Generated by Django 3.1.4 on 2021-02-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_workdetails_jobdes'),
    ]

    operations = [
        migrations.AddField(
            model_name='workdetails',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]