# Generated by Django 4.1.3 on 2023-05-19 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0006_domainlist_doamin_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domainlist',
            name='doamin_name',
        ),
        migrations.AddField(
            model_name='analysislist',
            name='doamin_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='域名'),
        ),
    ]
