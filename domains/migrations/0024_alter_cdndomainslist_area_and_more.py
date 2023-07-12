# Generated by Django 4.1.3 on 2023-07-03 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0023_cdndomainslist_origins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdndomainslist',
            name='area',
            field=models.CharField(choices=[('mainland', '中国境内加速'), ('overseas', '中国境外加速'), ('mainland_china', '中国大陆'), ('outside_mainland_china', '中国大陆境外'), ('global', '全球加速')], max_length=32, verbose_name='加速区域'),
        ),
        migrations.AlterField(
            model_name='cdndomainslist',
            name='servicetype',
            field=models.CharField(choices=[('web', '静态加速'), ('download', '下载加速'), ('media', '流媒体点播加速'), ('hybrid', '动静加速'), ('dynamic', '动态加速'), ('video', '点播加速'), ('wholeSite', '全站加速')], max_length=32, verbose_name='业务类型'),
        ),
        migrations.AlterField(
            model_name='cdndomainslist',
            name='status',
            field=models.CharField(choices=[('rejected', '域名审核未通过，域名备案过期/被注销导致'), ('processing', '部署中'), ('configuring', '配置中'), ('configure_failed', '配置失败'), ('checking', '审核中'), ('check_failed', '审核未通过'), ('deleting', '删除中'), ('closing', '关闭中'), ('online', '已启动'), ('offline', '已关闭')], max_length=32, verbose_name='加速服务状态'),
        ),
    ]