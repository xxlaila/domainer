# -*- coding: utf-8 -*-
"""
@File    : domain_list.py
@Time    : 2023/5/19 11:33 上午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import serializers
from domains.models.domain_list import DomainList, Status_CHOICES, \
    SearchEnginePush_CHOICES, CLOUD_CHOICES

class DomainListSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Status_CHOICES, help_text="状态")
    status_label = serializers.ChoiceField(choices=Status_CHOICES, source='get_status_display', help_text="状态")
    searchenginepush = serializers.ChoiceField(choices=SearchEnginePush_CHOICES, help_text="搜索引擎推送优化")
    searchenginepush_label = serializers.ChoiceField(choices=SearchEnginePush_CHOICES,
                                                     source='get_searchenginepush_display', help_text="搜索引擎推送优化")
    cloud = serializers.ChoiceField(choices=CLOUD_CHOICES, help_text="云")
    cloud_label = serializers.ChoiceField(choices=CLOUD_CHOICES, source='get_cloud_display', help_text="云")
    createdon = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', help_text="添加时间")
    updatedon = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', help_text="更新时间")

    class Meta:
        model = DomainList
        fields = '__all__'