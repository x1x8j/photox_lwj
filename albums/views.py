from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Album
from .serializers import AlbumCreateSerializer, AlbumSerializer
from images.models import Image


class AlbumView(APIView):
    permission_classes = [IsAuthenticated]

    # 自定义分页类
    class CustomPagination(PageNumberPagination):
        page_size = 10  # 默认每页显示10个相册
        page_size_query_param = 'page_size'  # 可以通过 query 参数自定义每页数量
        max_page_size = 50  # 最大每页50个相册

    pagination_class = CustomPagination

    def get(self, request):
        """
        获取当前用户的相册列表
        """
        user = self.request.user
        albums = Album.objects.filter(user=user).order_by('-created_at')

        # 使用分页器
        paginator = self.pagination_class()
        paginated_albums = paginator.paginate_queryset(albums, request)
        serializer = AlbumSerializer(paginated_albums, many=True)

        return paginator.get_paginated_response({
            "code": 0,
            "message": "Success",
            "data": serializer.data
        })

    def post(self, request):
        """
        创建一个新相册
        """
        serializer = AlbumCreateSerializer(data=request.data)
        if serializer.is_valid():
            # 保存时自动绑定当前用户
            album = serializer.save(user=request.user)
            return Response({
                "code": 0,
                "message": "Album created",
                "data": AlbumCreateSerializer(album).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "code": 1,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AlbumDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, album_id):
        """
        获取相册详情（包含图片列表）
        """
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({"code": 1, "message": "Album not found"}, status=status.HTTP_404_NOT_FOUND)

        # 认证检查：如果相册是私有的，必须是相册的所有者或认证用户才能查看
        if not album.is_public and album.user != request.user:
            raise PermissionDenied("You do not have permission to view this album.")


        # 序列化相册数据
        album_serializer = AlbumSerializer(album)

        return Response({
            "code": 0,
            "message": "Success",
            "data": {
                "album": album_serializer.data
            }
        }, status=status.HTTP_200_OK)

    def put(self, request, album_id):
        """
        修改相册信息
        """
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({"code": 1, "message": "Album not found"}, status=status.HTTP_404_NOT_FOUND)

        # 认证检查：只有相册所有者才能修改
        if album.user != request.user:
            raise PermissionDenied("You do not have permission to edit this album.")

        # 使用序列化器更新相册信息
        serializer = AlbumCreateSerializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            updated_album = serializer.save()
            return Response({
                "code": 0,
                "message": "Success",
                "data": AlbumCreateSerializer(updated_album).data
            }, status=status.HTTP_200_OK)

        return Response({
            "code": 1,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, album_id):
        """
        删除相册
        """
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({"code": 1, "message": "Album not found"}, status=status.HTTP_404_NOT_FOUND)

        # 认证检查：只有相册所有者才能删除相册
        if album.user != request.user:
            raise PermissionDenied("You do not have permission to delete this album.")

        # 删除相册
        album.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class AlbumAddImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, album_id):
        # 检查相册是否存在且属于当前用户
        try:
            album = Album.objects.get(id=album_id, user=request.user)
        except Album.DoesNotExist:
            return Response({
                "code": 1,
                "message": "Album not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # 获取图片对象
        image_id = request.data.get('image_id')
        try:
            image = Image.objects.get(id=image_id, user=request.user)  # 确保图片属于当前用户
        except Image.DoesNotExist:
            return Response({
                "code": 1,
                "message": "Image not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # 将图片添加到相册
        album.images.add(image)

        return Response({
            "code": 0,
            "message": "Image added to album"
        }, status=status.HTTP_200_OK)


class AlbumRemoveImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, album_id):
        # 检查相册是否存在且属于当前用户
        try:
            album = Album.objects.get(id=album_id, user=request.user)
        except Album.DoesNotExist:
            return Response({
                "code": 1,
                "message": "Album not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # 获取图片对象
        image_id = request.data.get('image_id')
        try:
            image = Image.objects.get(id=image_id, user=request.user)  # 确保图片属于当前用户
        except Image.DoesNotExist:
            return Response({
                "code": 1,
                "message": "Image not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if image not in album.images.all():
            return Response({
                "code": 1,
                "message": "Image not in this album"
            }, status=status.HTTP_400_BAD_REQUEST)

        # 将图片从相册中移除
        album.images.remove(image)

        return Response({
            "code": 0,
            "message": "Image removed from album"
        }, status=status.HTTP_200_OK)

