from django.db import models

# Create your models here.
# community/models.py
from django.db import models
from django.conf import settings
# 从 albums app 导入 Album 模型
from albums.models import Album

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE, verbose_name="评论用户")
    # 评论关联到相册
    album = models.ForeignKey(Album, related_name='comments', on_delete=models.CASCADE, verbose_name="所属相册")
    content = models.TextField(verbose_name="评论内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.album.title}"

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE, verbose_name="点赞用户")
    # 点赞关联到相册
    album = models.ForeignKey(Album, related_name='likes', on_delete=models.CASCADE, verbose_name="所属相册")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    # 确保同一个用户对同一个相册只能点赞一次
    class Meta:
        unique_together = ('user', 'album')
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"Like by {self.user.username} on {self.album.title}"