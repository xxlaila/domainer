# Generated by Django 4.1.3 on 2023-05-19 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainlist',
            name='effectivedns',
            field=models.CharField(blank=True, max_length=258, null=True, verbose_name='有效DNS'),
        ),
    ]