# Generated by Django 4.1.3 on 2023-06-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0015_alter_analysislist_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysislist',
            name='status',
            field=models.IntegerField(choices=[(1, 'Enable'), (2, 'Disable')], verbose_name='记录状态'),
        ),
    ]