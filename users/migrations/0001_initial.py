# Generated by Django 4.1.3 on 2023-07-19 04:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='中文名')),
                ('english_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='英文名')),
                ('mailbox', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('eid', models.IntegerField(blank=True, null=True, verbose_name='工号')),
                ('phone', models.IntegerField(blank=True, null=True, verbose_name='电话')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('is_active', models.IntegerField(blank=True, default=1, null=True, verbose_name='用户状态')),
                ('is_authenticated', models.IntegerField(blank=True, default=1, null=True, verbose_name='登录状态')),
                ('is_super', models.IntegerField(blank=True, default=0, null=True, verbose_name='管理员')),
                ('is_staff', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'Users',
                'verbose_name_plural': 'Users',
                'ordering': ['-name'],
            },
        ),
    ]