from rest_framework import serializers
from .models import Album
from images.serializers import ImageSerializer

class AlbumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']
        read_only_fields = ['id', 'created_at']

class AlbumSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)  # 关联图片序列化
    class Meta:
        model = Album
        fields = ['id', 'title', 'description', 'is_public', 'created_at', 'images']