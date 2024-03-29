# Generated by Django 3.1.4 on 2021-03-06 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210305_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='workdetails',
            name='verify_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='workdetails',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workdetails',
            name='company_website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workdetails',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workdetails',
            name='job_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='workdetails',
            name='job_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
