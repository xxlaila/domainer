# -*- coding: utf-8 -*-
"""
@File    : additive_solution.py
@Time    : 2023/1/16 3:48 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import serializers
from settings.models.additive_solution import AdditiveSolution


class AdditiveSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditiveSolution
        fields = '__all__'