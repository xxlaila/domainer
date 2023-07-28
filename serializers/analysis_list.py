# -*- coding: utf-8 -*-
"""
@File    : analysis_list.py
@Time    : 2023/5/19 11:38 上午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import serializers
from domains.models.analysis_list import AnalysisList, \
    MonitorStatus__CHOICES, CLOUD_CHOICES, STATUS_CHOICES


class AnalysisListSerializer(serializers.ModelSerializer):
    monitorstatus = serializers.ChoiceField(choices=MonitorStatus__CHOICES, help_text="记录监控状态")
    monitorstatus_label = serializers.ChoiceField(choices=MonitorStatus__CHOICES,
                                                     source='get_monitorstatus_display', help_text="记录监控状态")
    cloud = serializers.ChoiceField(choices=CLOUD_CHOICES, help_text="云")
    cloud_label = serializers.ChoiceField(choices=CLOUD_CHOICES, source='get_cloud_display', help_text="云")
    status = serializers.ChoiceField(choices=STATUS_CHOICES, help_text="状态")
    status_label = serializers.ChoiceField(choices=STATUS_CHOICES, source='get_status_display', help_text="状态")
    secordid = serializers.SerializerMethodField()
    updatedon = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', help_text="更新时间", read_only=True)
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    def get_secordid(self, obj):
        return str(obj.secordid)

    class Meta:
        model = AnalysisList
        fields = '__all__'