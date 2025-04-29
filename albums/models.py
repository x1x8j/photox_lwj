from django.db import models

# Create your models here.
# albums/models.py
from django.db import models
from django.conf import settings
# 从 images app 导入 Image 模型
from images.models import Image

class Album(models.Model):
    title = models.CharField(max_length=255, verbose_name="相册标题")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='albums', on_delete=models.CASCADE, verbose_name="所属用户")
    # 使用 ManyToManyField 将图片关联到相册
    images = models.ManyToManyField(Image, related_name='albums', blank=True, verbose_name="包含图片")
    is_public = models.BooleanField(default=False, verbose_name="是否公开")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相册"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']