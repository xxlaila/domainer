# -*- coding: utf-8 -*-
"""
@File    : healthchecklog.py
@Time    : 2023/7/17 3:14 下午
@Author  : xxlaila
@Software: PyCharm
"""

import logging

class HealthCheckLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 检查请求路径是否是健康检查路径
        if request.path == '/health-check/':
            # 禁止在健康检查请求上打印日志
            logging.disable(logging.INFO)  # 禁用 INFO 级别及以下的日志记录
        else:
            logging.disable(logging.NOTSET)  # 启用所有日志记录

        response = self.get_response(request)

        return response
