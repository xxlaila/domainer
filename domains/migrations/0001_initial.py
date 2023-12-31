# Generated by Django 4.1.3 on 2023-07-19 04:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('defaultns', models.CharField(blank=True, max_length=32, null=True, verbose_name='默认记录')),
                ('domainid', models.CharField(blank=True, max_length=256, null=True, verbose_name='域名标识')),
                ('line', models.CharField(blank=True, max_length=32, null=True, verbose_name='线路')),
                ('lineid', models.CharField(blank=True, max_length=32, null=True, verbose_name='线路Id')),
                ('mx', models.CharField(blank=True, max_length=32, null=True, verbose_name='MX值')),
                ('monitorstatus', models.CharField(choices=[('OK', '正常'), ('WARN', '告警'), ('DOWN', '宕机')], max_length=12, verbose_name='记录监控状态')),
                ('subdomain', models.CharField(blank=True, max_length=64, null=True, verbose_name='主机名')),
                ('secordid', models.BigIntegerField(blank=True, null=True, verbose_name='记录Id')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(1, 'Enable'), (0, 'Disable')], verbose_name='记录状态')),
                ('ttl', models.CharField(blank=True, max_length=12, null=True, verbose_name='缓存时间')),
                ('type', models.CharField(blank=True, max_length=32, null=True, verbose_name='记录类型')),
                ('updatedon', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('value', models.CharField(blank=True, max_length=128, null=True, verbose_name='记录值')),
                ('weight', models.CharField(blank=True, max_length=32, null=True, verbose_name='记录权重')),
                ('cloud', models.CharField(choices=[('Tencent', '腾讯云'), ('Huawei', '华为云'), ('Aliyun', '阿里云')], db_index=True, max_length=32, verbose_name='云')),
                ('domain_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='域名')),
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='创建人')),
                ('editd_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='修改人')),
                ('demand_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='需求人')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': 'AnalysisList',
                'verbose_name_plural': 'AnalysisList',
                'ordering': ['-updated_time'],
            },
        ),
        migrations.CreateModel(
            name='CdnDomainsList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('resourceid', models.CharField(blank=True, max_length=64, null=True, verbose_name='域名ID')),
                ('domain', models.CharField(blank=True, db_index=True, max_length=256, null=True, verbose_name='加速域名')),
                ('cname', models.CharField(blank=True, db_index=True, max_length=512, null=True, verbose_name='CNAME 地址')),
                ('status', models.CharField(choices=[('rejected', '域名审核未通过，域名备案过期/被注销导致'), ('processing', '部署中'), ('configuring', '配置中'), ('configure_failed', '配置失败'), ('checking', '审核中'), ('check_failed', '审核未通过'), ('deleting', '删除中'), ('closing', '关闭中'), ('online', '已启动'), ('offline', '已关闭')], max_length=32, verbose_name='加速服务状态')),
                ('servicetype', models.CharField(choices=[('web', '静态加速'), ('download', '下载加速'), ('media', '流媒体点播加速'), ('hybrid', '动静加速'), ('dynamic', '动态加速'), ('video', '点播加速'), ('wholeSite', '全站加速')], max_length=32, verbose_name='业务类型')),
                ('origin', models.TextField(blank=True, null=True, verbose_name='源站配置详情')),
                ('origins', models.TextField(blank=True, null=True, verbose_name='回源地址')),
                ('disable', models.CharField(choices=[('normal', '正常状态'), ('overdue', '账号欠费导致域名关闭，充值完成后可自行启动加速服务'), ('malicious', '域名出现恶意行为，强制关闭加速服务'), ('ddos', '域名被大规模 DDoS 攻击，关闭加速服务'), ('idle', '域名超过 90 天内无任何操作、数据产生，判定为不活跃域名自动关闭加速服务，可自行启动加速服务'), ('unlicensed', '域名未备案 / 备案注销，自动关闭加速服务，备案完成后可自行启动加速服务'), ('capping', '触发配置的带宽阈值上限'), ('readonly', '域名存在特殊配置，被锁定')], max_length=32, verbose_name='封禁状态')),
                ('area', models.CharField(choices=[('mainland', '中国境内加速'), ('overseas', '中国境外加速'), ('mainland_china', '中国大陆'), ('outside_mainland_china', '中国大陆境外'), ('global', '全球加速')], max_length=32, verbose_name='加速区域')),
                ('readonly', models.CharField(choices=[('normal', '未锁定'), ('mainland', '中国境内锁定'), ('overseas', '中国境外锁定'), ('global', '全球锁定')], max_length=32, verbose_name='锁定状态')),
                ('product', models.CharField(blank=True, max_length=16, null=True, verbose_name='所属产品')),
                ('parentHost', models.CharField(blank=True, max_length=128, null=True, verbose_name='主域名')),
                ('cloud', models.CharField(choices=[('Tencent', '腾讯云'), ('Huawei', '华为云'), ('Aliyun', '阿里云')], db_index=True, max_length=32, verbose_name='云')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': 'CdnDomainsList',
                'verbose_name_plural': 'CdnDomainsList',
                'ordering': ['-domain'],
            },
        ),
        migrations.CreateModel(
            name='DomainAudit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='域名')),
                ('domainid', models.CharField(blank=True, max_length=256, null=True, verbose_name='域名标识')),
                ('cloud', models.CharField(choices=[('Tencent', '腾讯云'), ('Huawei', '华为云'), ('Aliyun', '阿里云')], db_index=True, max_length=32, verbose_name='云')),
                ('secordid', models.BigIntegerField(blank=True, null=True, verbose_name='记录Id')),
                ('source_record', models.TextField(blank=True, null=True, verbose_name='源记录')),
                ('news_record', models.TextField(blank=True, null=True, verbose_name='新记录')),
                ('action', models.CharField(blank=True, max_length=16, null=True, verbose_name='动作')),
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='修改人')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'DomainAudit',
                'verbose_name_plural': 'DomainAudit',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='DomainList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('domainid', models.CharField(blank=True, max_length=256, null=True, verbose_name='域名标识')),
                ('effectivedns', models.CharField(blank=True, max_length=258, null=True, verbose_name='有效DNS')),
                ('isvip', models.CharField(blank=True, max_length=16, null=True, verbose_name='付费套餐')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='名称')),
                ('owner', models.CharField(blank=True, max_length=128, null=True, verbose_name='所属账号')),
                ('punycode', models.CharField(blank=True, max_length=64, null=True, verbose_name='punycode编码')),
                ('recordCount', models.IntegerField(blank=True, null=True, verbose_name='记录数量')),
                ('remark', models.CharField(blank=True, max_length=64, null=True, verbose_name='备注')),
                ('searchenginepush', models.CharField(blank=True, choices=[('Yes', '是'), ('No', '否')], max_length=64, null=True, verbose_name='搜索引擎推送优化')),
                ('status', models.CharField(blank=True, choices=[('ENABLE', '正常'), ('PAUSE', '暂停'), ('SPAM', '封禁')], max_length=12, null=True, verbose_name='状态')),
                ('createdon', models.DateTimeField(auto_now_add=True, null=True, verbose_name='添加时间')),
                ('updatedon', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('vipautorenew', models.CharField(blank=True, max_length=32, null=True, verbose_name='开通VIP自动续费')),
                ('cloud', models.CharField(choices=[('Tencent', '腾讯云'), ('Huawei', '华为云'), ('Aliyun', '阿里云')], db_index=True, max_length=32, verbose_name='云')),
            ],
            options={
                'verbose_name': 'DomainList',
                'verbose_name_plural': 'DomainList',
                'ordering': ['name', '-name', models.OrderBy(models.F('recordCount'), descending=True, nulls_last=True)],
            },
        ),
    ]
