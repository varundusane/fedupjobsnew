# Generated by Django 3.1.4 on 2021-04-19 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210306_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workdetails',
            name='verify',
            field=models.BooleanField(default=True),
        ),
    ]
