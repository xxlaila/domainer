# Generated by Django 4.1.3 on 2023-07-28 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloud_secret',
            name='tags',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='标签'),
        ),
    ]
