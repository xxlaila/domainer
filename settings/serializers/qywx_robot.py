# -*- coding: utf-8 -*-
"""
@File    : qywx_robot.py
@Time    : 2023/3/9 2:11 下午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework import serializers
from settings.models.qywx_robot import QywxRobot


class QywxRobotSerializer(serializers.ModelSerializer):
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = QywxRobot
        fields = '__all__'