# -*- coding: utf-8 -*-
"""
@File    : celery.py
@Time    : 2023/2/27 11:20 上午
@Author  : xxlaila
@Software: PyCharm
"""

from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

envir = os.getenv("ENV", "test")
if envir == "test":
    from domainer.settings.test import *
else:
    from domainer.settings.prod import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'domainer.settings.{envir}')

backend = CELERY_CONFIG["BROKER_URL"]
broker = CELERY_CONFIG["RESULT_BACKEND"]
app = Celery('domainer', backend=backend, broker=broker, )
app.conf.timezone = 'Asia/Shanghai'

class Config:
    # result_backend = 'django-db'  #使用django orm 作为结果存储
    broker_url = CELERY_CONFIG["BROKER_URL"]   # 任务队列的位置
    result_backend = CELERY_CONFIG["RESULT_BACKEND"]   # 任务执行结果存放
    accept_content = ['application/json']   # 配置celery可以接受哪些格式
    beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
    result_serializer = "json"  # 结果序列化数据格式
    result_compression = 'zlib' #是否压缩
    worker_concurrency = 2  #并发数默认已CPU数量定
    worker_prefetch_multiplier = 2  #celery worker 每次去redis取任务的数量
    worker_max_tasks_per_child = 3  #每个worker最多执行3个任务就摧毁，避免内存泄漏
    worker_max_memory_per_child = 12000  # 显示内存12MB
    # enable_utc = False  #关闭时区
    # timezone = 'Asia/Shanghai' # 项目中有定时任务 设置时区  这里跟项目一致
    result_expires = 1800


app.config_from_object(Config)
app.autodiscover_tasks()
# app.now = timezone.now()
app.config_from_object('domainer.celery')