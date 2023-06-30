# -*- coding: utf-8 -*-
"""
@File    : page.py
@Time    : 2023/2/27 12:12 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


# 基本分页
class CustomNumberPagination(PageNumberPagination):
    page_size = 10  # 每页显示10条
    page_query_param = 'page'   # 查询第几页的参数 ?page=3

    max_page_size = 20  # 每页最大显示多少条
    page_size_query_param = 'size'  #每页显示的条数查询条件（默认是page_size显示的条数） # ?page=2&size=3

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            "data": {
                'count': self.page.paginator.count,
                'results': data,
            }
        })


# 偏移分页
class CustomLimitOffsetPagtion(LimitOffsetPagination):
    default_limit = 10  # 默认显示几条
    limit_query_param = 'limit'  # ？limit=10   表示取10条
    offset_query_param = 'offset'  # 偏移  ?offset=20&limit=10   从第20个位置开始，取11条数据
    max_limit = 20  # 最多显示20条
