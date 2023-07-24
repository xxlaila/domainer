# -*- coding: utf-8 -*-
"""
@File    : loginrequired.py
@Time    : 2023/3/3 2:53 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.shortcuts import redirect
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
import json
from urllib.parse import unquote_plus
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

from users.models.users import Users
from django.utils import timezone


class BaseResponse(JsonResponse):
    def __init__(self, data, code=None, msg=None, **kwargs):
        data = {
            'code': code if code is not None else 0,
            'msg': msg if msg is not None else 'success',
            'data': data
        }
        super().__init__(data, **kwargs)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        # 开放白名单，比如['/login/', '/admin/']
        self.open_urls = [self.login_url] + getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request):
        old = request.META
        TOKEN = request.COOKIES.get('TOKEN')
        if TOKEN and str(TOKEN) == settings.API_TOKEN:
            try:
                user = User.objects.get(username=settings.API_USERNAME)
            except User.DoesNotExist:
                user = User(username=settings.API_USERNAME, last_name=settings.API_USER_LASTNAME)
                user.last_login = timezone.now()
                user.save()
            request.user = user
            response = self.get_response(request)
            return response
        if request.path_info.find('admin') == 1 or request.path_info.find('swagger') == 1:
            if not cache.get(request.COOKIES.get('OA-Hash')):
                if not request.user.is_authenticated and request.path_info not in self.open_urls:
                    return redirect(self.login_url)
        elif request.path_info.find('health-check') == 1:
            return self.get_response(request)
        elif request.path_info.find('receive') > 1:
            return self.get_response(request)
        elif "swagger" in old["PATH_INFO"]:
            if cache.get("PATH_INFO"):
                cache.set("PATH_INFO", old["PATH_INFO"], 1800)
                request.token = cache.get("PATH_INFO")
                return self.get_response(request)
        else:
            user = None
            if not request.COOKIES:
                return BaseResponse(data="", code=403, msg="not sign in", status=200)
            else:
                cks = request.COOKIES
                cks_json = json.dumps(cks)
                cache_key = request.COOKIES.get('OA-Hash')
                u_name = request.COOKIES.get('OA-Name')
                eid = request.COOKIES.get('OA-EID')
                mailbox = request.COOKIES.get('OA-EMail')
                if request.COOKIES.get('OA-EMail'):
                    english_name = request.COOKIES.get('OA-EMail').split('@')[0]
                else:
                    english_name = ''
                if not all([cache_key, u_name, eid, mailbox]):
                    logger.error("获取cooike为空")
                    return BaseResponse(data="", code=403, msg="not sign in!", status=200)
                _username = unquote_plus(u_name)
                logger.debug(f"request.COOKIES:{cks}, cache_key:{cache_key},u_name:{u_name}, "
                             f"eid:{eid},mailbox:{mailbox}, _username: {_username}, english_name: {english_name}")

                data = {"name": _username, 'english_name': english_name, "mailbox": mailbox}
                user = Users.objects.filter(eid=eid, english_name=data['english_name']).first()
                if cache.get(cache_key):
                    Users.objects.update_or_create(eid=eid, **data)
                    cache.set(request.COOKIES.get('OA-Hash'), request.headers.get('Cookie'), 1800)
                else:
                    try:
                        Users.objects.update_or_create(eid=eid, **data)
                        cache.set(request.COOKIES.get('OA-Hash'), request.headers.get('Cookie'), 1800)
                    except Exception as e:
                        logger.error("添加登录用户失败，失败原因是：{},\n用户信息是{}".format(e, data.update({"eid": eid})))
                        return BaseResponse(data="", code=18456, msg="用户登录失败!", status=200)
                request.username = user
        return self.get_response(request)
