# image_repo_backend/settings.py
import os
from datetime import timedelta
from pathlib import Path
# 如果你使用 .env 文件管理敏感信息 (推荐)
from dotenv import load_dotenv
load_dotenv() # 加载 .env 文件

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# 最好从环境变量读取
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*'] # 开发时可以用 '*'，生产环境需要配置具体的域名


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三方应用
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders', # 如果需要跨域访问API，需要安装 pip install django-cors-headers
    'drf_yasg',    # Swagger API 文档

    # 你自己的应用 (使用 .apps 文件里的 AppConfig 名称，或者直接用应用名)
    'users.apps.UsersConfig',
    'images.apps.ImagesConfig',
    'albums.apps.AlbumsConfig',
    'community.apps.CommunityConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS 中间件，应放在 CommonMiddleware 前面
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'image_repo_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'image_repo_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# 默认 SQLite 配置
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# ---> Database (改为 MySQL 配置) <---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',         # 修改 ENGINE
        'NAME': os.environ.get('MYSQL_DATABASE'),     # 读取 MySQL 环境变量
        'USER': os.environ.get('MYSQL_USER'),         # 读取 MySQL 环境变量
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'), # 读取 MySQL 环境变量
        'HOST': 'db',                                # Docker 服务名不变
        'PORT': '3306',                             # MySQL 默认端口
        # 'OPTIONS': { # 可选：如果需要指定字符集等
        #     'charset': 'utf8mb4',
        # },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # ... (保持默认即可)
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans' # 设置为中文

TIME_ZONE = 'Asia/Shanghai' # 设置为中国时区

USE_I18N = True

USE_TZ = True # 建议保持 True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles' # 生产环境收集静态文件用

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # 用户上传文件（如头像）的本地存储路径

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- 自定义配置 ---

# 指定使用你的 CustomUser 模型
AUTH_USER_MODEL = 'users.CustomUser'

# DRF 配置
REST_FRAMEWORK = {
    # API 权限控制 (全局默认，可以在视图中覆盖)
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated', # 全局要求登录才能访问
        'rest_framework.permissions.AllowAny',       # 全局允许任何人访问 (更灵活，在视图中单独加权限)
    ],
    # API 认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 如果需要 Session 认证 (比如用于 Django Admin 或 浏览器调试 API)
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    # 分页配置 (可选)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10 # 每页默认显示10条
}


# Simple JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),      # Access Token 有效期1天
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh Token 有效期7天
    'ROTATE_REFRESH_TOKENS': False,                  # 是否刷新 Refresh Token
    'BLACKLIST_AFTER_ROTATION': False,               # Refresh Token 刷新后是否加入黑名单
    'UPDATE_LAST_LOGIN': False,                      # 验证成功后是否更新 last_login 字段

    'ALGORITHM': 'HS256',                            # 加密算法
    # JWT 签名密钥，应从环境变量读取，且与 SECRET_KEY 不同
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),                # 请求头中 Token 类型，例如: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',        # 请求头字段名
    'USER_ID_FIELD': 'id',                           # Token 中标识用户的字段
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),  # 滑动窗口 Token 的有效期
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1), # 滑动窗口 Token 的刷新有效期
}


# CORS 配置 (如果前端和后端不在同一个域)
# 需要 pip install django-cors-headers 并在 INSTALLED_APPS 和 MIDDLEWARE 中添加
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # 你的前端开发地址
    "http://127.0.0.1:8080",
    # 添加其他允许访问的源
]
# 或者允许所有源 (开发时方便，生产环境不推荐)
# CORS_ALLOW_ALL_ORIGINS = True

# 允许携带 Cookie (如果需要跨域 Session 或 CSRF)
# CORS_ALLOW_CREDENTIALS = True




# 七牛云配置 (从环境变量读取)
QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME')
QINIU_BUCKET_URL = os.getenv('QINIU_BUCKET_URL') # 例如: http://your_bucket.example.com

# 如果需要使用 .env 文件，确保在项目根目录创建 .env 文件并写入类似内容:
# DJANGO_SECRET_KEY=your_strong_secret_key
# JWT_SECRET_KEY=your_other_strong_secret_key
# DB_NAME=photox_db
# DB_USER=photox_user
# DB_PASSWORD=your_db_password
# DB_HOST=127.0.0.1
# DB_PORT=3306
# QINIU_ACCESS_KEY=your_qiniu_ak
# QINIU_SECRET_KEY=your_qiniu_sk
# QINIU_BUCKET_NAME=your_qiniu_bucket_name
# QINIU_BUCKET_URL=http://your_qiniu_bucket_domain

