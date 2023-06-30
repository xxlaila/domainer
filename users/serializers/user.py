# -*- coding: utf-8 -*-
"""
@File    : user.py
@Time    : 2022/11/30 6:52 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
