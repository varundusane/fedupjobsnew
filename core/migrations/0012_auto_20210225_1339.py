# Generated by Django 3.1.4 on 2021-02-25 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_workdetails_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workdetails',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
