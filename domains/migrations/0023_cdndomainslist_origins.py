# Generated by Django 4.1.3 on 2023-06-30 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0022_cdndomainslist_alter_analysislist_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdndomainslist',
            name='origins',
            field=models.TextField(blank=True, null=True, verbose_name='回源地址'),
        ),
    ]