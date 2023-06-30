# -*- coding: utf-8 -*-
"""
@File    : logging.py
@Time    : 2023/4/19 2:23 下午
@Author  : xxlaila
@Software: PyCharm
"""
import os
envir = os.getenv("ENV", "test")
if envir == "test":
    BASE_DIR = "/opt/logs/"
else:
    BASE_DIR = "/data/logs/"

DOMAINER_LOG_FILE = os.environ.get('DOMAINER_LOG_FILE', os.path.join(BASE_DIR, 'ops-domainer-api', 'ops-domainer-api.log'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '[%(asctime)s] [%(name)s:%(lineno)s] [%(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'file': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*50,
            'backupCount': 7,
            'formatter': 'main',
            'filename': DOMAINER_LOG_FILE,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'domainer': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
