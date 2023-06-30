# -*- coding: utf-8 -*-
"""
@File    : cloud_secret.py
@Time    : 2023/3/9 2:10 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import serializers
from settings.models.cloud_secret import Cloud_Secret
from showsql.models.slow_results import CLOUD_CHOICES

class CloudSecretSerializer(serializers.ModelSerializer):
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    name = serializers.ChoiceField(choices=CLOUD_CHOICES, help_text="所属云")
    name_label = serializers.ChoiceField(choices=CLOUD_CHOICES, read_only=True,
                                         source='get_name_display', help_text="所属云")

    class Meta:
        model = Cloud_Secret
        fields = '__all__'

