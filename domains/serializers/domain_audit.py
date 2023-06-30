# -*- coding: utf-8 -*-
"""
@File    : domain_audits.py
@Time    : 2023/5/26 10:35 上午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import serializers
from domains.models.domain_audit import DomainAudit,  CLOUD_CHOICES


class DomainAuditSerializer(serializers.ModelSerializer):
    cloud = serializers.ChoiceField(choices=CLOUD_CHOICES, help_text="云")
    #cloud_label = serializers.ChoiceField(choices=CLOUD_CHOICES, source='get_cloud_display', help_text="云")
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = DomainAudit
        fields = '__all__'