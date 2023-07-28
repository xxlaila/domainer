# -*- coding: utf-8 -*-
"""
@File    : cdndomain_list.py
@Time    : 2023/6/30 12:21 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import serializers
from domains.models.cdndomain_list import CdnDomainsList, \
    READONLY_CHOICES, AREA_CHOICES, DISABLE_CHOICES, SERVICETYPE_CHOICES, STATUS_CHOICES


class CdnDomainsListSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=STATUS_CHOICES, help_text="状态")
    status_label = serializers.ChoiceField(choices=STATUS_CHOICES, source='get_status_display', help_text="状态")
    servicetype = serializers.ChoiceField(choices=SERVICETYPE_CHOICES, help_text="业务类型")
    servicetype_label = serializers.ChoiceField(choices=SERVICETYPE_CHOICES, source='get_servicetype_display',
                                                help_text="业务类型")
    disable = serializers.ChoiceField(choices=DISABLE_CHOICES, help_text="封禁状态")
    disable_label = serializers.ChoiceField(choices=DISABLE_CHOICES, source='get_disable_display', help_text="封禁状态")
    area = serializers.ChoiceField(choices=AREA_CHOICES, help_text="加速区域")
    area_label = serializers.ChoiceField(choices=AREA_CHOICES, source='get_area_display', help_text="加速区域")
    readonly = serializers.ChoiceField(choices=READONLY_CHOICES, help_text="锁定状态")
    readonly_label = serializers.ChoiceField(choices=READONLY_CHOICES, source='get_readonly_display',
                                             help_text="锁定状态")
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = CdnDomainsList
        fields = '__all__'
