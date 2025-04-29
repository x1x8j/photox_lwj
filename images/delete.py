
from django.conf import settings
import qiniu


def delete_image_from_cloud(image_url):
    # 获取图片的文件名或路径部分
    file_name = image_url.split('/')[-1]

    # 从 settings.py 中获取七牛云的认证信息
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    bucket_name = settings.QINIU_BUCKET_NAME

    # 创建七牛云认证对象
    q = qiniu.Auth(access_key, secret_key)
    bucket = qiniu.BucketManager(q)

    # 删除图片
    ret, info = bucket.delete(bucket_name, file_name)
    if info.status_code != 200:
        raise Exception("Failed to delete image from cloud storage")
