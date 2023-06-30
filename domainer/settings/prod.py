# -*- coding: utf-8 -*-
"""
@File    : prod.py
@Time    : 2023/2/27 11:17 上午
@Author  : xxlaila
@Software: PyCharm
"""

import os
from .base import *
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'domainer',  # 数据库名称，需要自己定义
        'USER': 'domainer',
        'PASSWORD': 'domainer',  # 管理员账号密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/10",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": True,
            "PASSWORD": "123456",
        }
    }
}

CELERY_CONFIG = {
    "BROKER_URL": 'redis://:123456@127.0.0.1:6379/10',
    "RESULT_BACKEND": 'redis://:123456@127.0.0.1:6379/10'
}