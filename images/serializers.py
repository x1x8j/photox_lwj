from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields=['id', 'image_url', 'title', 'tags', 'user', 'created_at','is_public']

class ImageUploadSerializer(serializers.Serializer):
    image=serializers.ImageField()
    title = serializers.CharField(required=False, max_length=255)
    is_public = serializers.BooleanField(required=False, default=False)