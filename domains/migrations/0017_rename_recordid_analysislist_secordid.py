# Generated by Django 4.1.3 on 2023-06-21 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0016_alter_analysislist_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysislist',
            old_name='recordid',
            new_name='secordid',
        ),
    ]
