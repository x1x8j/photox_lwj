from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
# from django.contrib.auth import get_user_model
from .models import CustomUser

# User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    用户注册视图
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,) # 允许任何人访问注册接口
    serializer_class = RegisterSerializer

    # 重写 create 方法来自定义成功响应 (可选)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 不在响应中返回用户信息或 token，只返回成功消息
        return Response({"code": 0, "message": "用户注册成功"}, status=status.HTTP_201_CREATED)


# Simple JWT 提供了登录视图，我们通常直接使用它，但如果你想自定义返回格式可以包装一下
# from rest_framework_simplejwt.views import TokenObtainPairView
# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 200:
#             # 自定义成功响应格式
#             return Response({
#                 "code": 0,
#                 "message": "登录成功",
#                 "data": response.data # access 和 refresh token
#             }, status=status.HTTP_200_OK)
#         return response # 返回默认的错误响应

# 获取当前用户信息的视图示例 (需要认证)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class CurrentUserView(APIView):
    """
    获取当前登录用户信息
    """
    permission_classes = [IsAuthenticated] # 要求用户必须登录

    def get(self, request):
        serializer = UserSerializer(request.user) # request.user 就是当前登录的用户对象
        return Response({"code": 0, "message": "获取成功", "data": serializer.data})