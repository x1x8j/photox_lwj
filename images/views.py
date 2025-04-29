# views.py
from django.conf import settings  # 导入 settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from ai_image import ai_image
from .delete import delete_image_from_cloud
from .models import Image
from .serializers import ImageUploadSerializer, ImageSerializer
from save import upload_and_set_metadata  # 七牛云上传工具
from .tasks import ai_image_analysis


def welcome_view(request):
    return HttpResponse("Welcome to Photox API!")

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]  # 只有认证用户才能上传
    parser_classes = [MultiPartParser]  # 处理 multipart/form-data 请求

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            # 获取上传的图片文件
            image_file = request.FILES['image']

            # 使用 FileSystemStorage 保存文件，生成临时路径
            fs = FileSystemStorage(location='/tmp')  # 存储到临时目录
            tmp_file_path = fs.save(image_file.name, image_file)  # 保存到临时目录
            tmp_file_path = fs.path(tmp_file_path)  # 获取文件的绝对路径

            # 使用原始图片名称或生成唯一文件名
            file_name = f"images/{image_file.name}"

            # 获取七牛云的配置
            access_key = settings.QINIU_ACCESS_KEY
            secret_key = settings.QINIU_SECRET_KEY
            bucket_name = settings.QINIU_BUCKET_NAME

            # 上传图片到七牛云并获取外链 URL
            tags, category = ai_image(tmp_file_path)
            image_url = upload_and_set_metadata(
                access_key=access_key,
                secret_key=secret_key,
                bucket_name=bucket_name,
                file_path=tmp_file_path,  # 传递临时文件的绝对路径
                key=file_name,  # 七牛云中的路径+文件名
                tags=tags,
                category=category
            )

            # 删除临时文件
            fs.delete(tmp_file_path)

            if not image_url:
                return Response({"error": "上传到七牛云失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 保存图片信息到数据库
            image = Image.objects.create(
                image_url=image_url,
                title=serializer.validated_data.get('title', ''),
                tags=tags,
                user=request.user,  # 上传者为当前认证的用户
                is_public=serializer.validated_data.get('is_public', False)
            )

            # 返回上传成功的响应，包含图片的外链 URL 和其他信息
            return Response({
                "code": 0,
                "message": "Image uploaded successfully",
                "data": ImageSerializer(image).data  # 返回图片的序列化数据
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageListView(ListAPIView):
    permission_classes = [IsAuthenticated]  # 确保用户认证
    serializer_class = ImageSerializer  # 使用已有的序列化器

    # 自定义分页类，控制每页返回的图片数量
    class CustomPagination(PageNumberPagination):
        page_size = 10  # 默认每页显示10个图片
        page_size_query_param = 'page_size'
        max_page_size = 50  # 最大每页50个图片

    pagination_class = CustomPagination

    def get_queryset(self):
        # 只获取当前用户上传的图片
        user = self.request.user
        queryset = Image.objects.filter(user=user)

        # 获取排序参数
        ordering = self.request.query_params.get('ordering', '-created_at')  # 默认按创建时间降序排序

        return queryset.order_by(ordering)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ImageDetailView(APIView):
    permission_classes = [IsAuthenticated]  # 需要认证

    # GET 请求，获取图片详情
    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response({"code": 1, "message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageSerializer(image)
        return Response({
            "code": 0,
            "message": "Success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # PUT 请求，修改图片信息
    def put(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response({"code": 1, "message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        if image.user != request.user:
            raise PermissionDenied("You do not have permission to edit this image.")

        title = request.data.get('title', None)
        is_public = request.data.get('is_public', None)

        if title:
            image.title = title
        if is_public is not None:
            image.is_public = is_public

        image.save()

        serializer = ImageSerializer(image)

        return Response({
            "code": 0,
            "message": "Success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response({"code": 1, "message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        # 只有图片的上传者可以删除该图片
        if image.user != request.user:
            raise PermissionDenied("You do not have permission to delete this image.")

        # # 删除图片文件（目前只实现了数据库的删除，七牛云上未删除）
        # delete_image_from_cloud(image.image_url)

        # 删除图片记录
        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

