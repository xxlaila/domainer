# Generated by Django 4.1.3 on 2023-06-27 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0019_alter_analysislist_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysislist',
            name='status',
            field=models.IntegerField(choices=[(1, 'Enable'), (0, 'Disable')], verbose_name='记录状态'),
        ),
    ]
