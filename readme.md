## 域名管理平台

#### 1、python 3.11
#### 6、域名管理平台，对接腾讯云和阿里云的所有域名，日志操作审计记录


### celery 定时任务
#### beat启动
celery -A domainer beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

#### work启动
celery -A domainer worker -l info

#### flower-celery监控
celery -A domainer flower --port=5555

### 需要执行静态资源迁移
python3 manage.py collectstatic
```angular2html
# 输入默认yes
```
**注**： 如做了前后端分离，配置文件做了多环境的区分，主配置文件的url 要增加：`re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.base.STATIC_ROOT}),`
主`settings 的base`文件要增加`STATIC_ROOT = os.path.join(BASE_DIR, 'static')`

### 多环境配置载入
```
# 测试使用
export ENV="test/prod"

# 生产使用
vim /etc/profile

export ENV=prod
```

### 创建数据库
```
create database domainer default character set utf8mb4 collate utf8mb4_unicode_ci;
create user 'domainer'@'%' identified by 'domainer'
grant all on domainer.* to 'domainer'@'%';
```