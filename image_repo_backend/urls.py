# image_repo_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView # 用于重定向

# --- Swagger ---
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Photox API",
        default_version='v1',
        description="Photox 项目 API 文档",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@example.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# --- Swagger End ---

urlpatterns = [
    # Admin 后台
    path('admin/', admin.site.urls),

    # path('api/v1/auth/', include('users.urls', namespace='users')),


    # --- API v1 URLs ---
    # 认证相关 (注册、登录、刷新 Token) -> 指向 users 应用的 urls.py
    # path('api/v1/auth/', include('users.urls.auth', namespace='auth')), # 建议将认证URL放入users/urls/auth.py
    path('api/v1/auth/', include('users.urls', namespace='auth')),
    # 用户信息相关 (获取/修改 'me') -> 指向 users 应用的 urls.py
    path('api/v1/users/', include('users.urls', namespace='users_profile')),
    # 图片相关 -> 指向 images 应用的 urls.py
    path('api/v1/images/', include('images.urls', namespace='images')),

    # 相册相关 -> 指向 albums 应用的 urls.py
    path('api/v1/albums/', include('albums.urls', namespace='albums')),

    # 社区相关 -> 指向 community 应用的 urls.py
    path('api/v1/community/', include('community.urls', namespace='community')),
    # --- API v1 URLs End ---


    # --- API 文档 ---
    # 根路径重定向到 Swagger UI
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'),
    # Swagger/Redoc 访问路径

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# 开发环境下，允许 Django 托管用户上传的媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # 如果需要Django处理静态文件