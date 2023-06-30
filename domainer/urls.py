"""domainer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.views.static import serve
from domainer import settings

schema_view = get_schema_view(
    openapi.Info(
        title="域名解析平台 API接口文档",  # 必传
        default_version="v1",  # 必传
        description="Welcome to the domainer",
        terms_of_service="http://127.0.0.1:8088/redoc",
        contact=openapi.Contact(email="ops@xxlaila.cn"),
        license=openapi.License(name="BSD LICENSE"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated,],
)

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls.api_urls', namespace='api-users')),
    path('settings/', include('settings.urls.api_urls', namespace='api-settings')),
    path('domains/', include('domains.urls.api_urls', namespace='api-domains')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path('swagger/',  schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('redoc/', schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.base.STATIC_ROOT}),

]

urlpatterns += static(settings.base.STATIC_ROOT, document_root=settings.base.STATIC_ROOT)
urlpatterns += router.urls