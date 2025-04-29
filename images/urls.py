
app_name = 'images'

from django.urls import path
from .views import ImageUploadView, ImageListView, ImageDetailView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('', ImageListView.as_view(), name='image-list'),
    path('<int:image_id>/', ImageDetailView.as_view(), name='image-detail-delete'),

]

# # images/urls.py
# from django.urls import path
# # 导入你的 images 应用下的视图（views）
# # 例如: from . import views
# # 或者导入具体的视图类/函数: from .views import ImageListView, ImageDetailView

# # --- 重要：定义应用命名空间 ---
# # 因为你在主 urls.py 的 include() 中使用了 namespace='images'，
# # 所以这里必须定义 app_name，并且值要匹配。
# app_name = 'images'

# urlpatterns = [
#     # --- 在这里定义你的图片相关的 URL 路由 ---

#     # 示例 (你需要根据你的 views.py 来替换):

#     # 比如，获取图片列表或上传图片 (对应 /api/v1/images/)
#     # path('', views.ImageListCreateAPIView.as_view(), name='image-list-create'),

#     # 比如，获取、更新、删除单个图片 (对应 /api/v1/images/<图片ID>/)
#     # path('<int:pk>/', views.ImageRetrieveUpdateDestroyAPIView.as_view(), name='image-detail'),

#     # 比如，点赞图片 (对应 /api/v1/images/<图片ID>/like/)
#     # path('<int:pk>/like/', views.like_image_view, name='image-like'),


#     # --- 请根据你的实际视图添加路由规则 ---
#     # 确保每个 path() 中的 name 参数在此文件内是唯一的，方便进行 URL 反向解析。

# ]

