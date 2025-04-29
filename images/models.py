from django.db import models

# Create your models here.
# images/models.py
from django.db import models
# 确保从 users app 导入 CustomUser
# from users.models import CustomUser
# 或者使用 settings.AUTH_USER_MODEL 避免循环导入
from django.conf import settings


class Image(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name="标题")
    # image_url 存储在云存储的地址
    image_url = models.URLField(max_length=1024, verbose_name="图片URL")
    # 使用 settings.AUTH_USER_MODEL 指向 CustomUser 模型
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images', on_delete=models.CASCADE, verbose_name="所属用户")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # AI 分析生成的标签
    tags = models.TextField(blank=True, null=True, verbose_name="AI标签")
    is_public = models.BooleanField(default=False)  # 个人图片默认私有

    def __str__(self):
        return self.title or f"Image {self.id}"

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']