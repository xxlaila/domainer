# -*- coding: utf-8 -*-
"""
@File    : zone.py
@Time    : 2023/3/9 2:09 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import serializers
from settings.models.zone import Zone
from showsql.models.slow_results import CLOUD_CHOICES

class ZoneSerializer(serializers.ModelSerializer):
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    cloud = serializers.ChoiceField(choices=CLOUD_CHOICES, help_text="所属云")
    cloud_label = serializers.ChoiceField(choices=CLOUD_CHOICES, source='get_cloud_display', help_text="所属云")

    class Meta:
        model = Zone
        fields = '__all__'