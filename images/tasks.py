from .models import Image
from image_classifier import ImageClassifier

def ai_image_analysis(path):

    # 初始化图像分类器
    classifier = ImageClassifier()

    # 使用分类器进行图像预测
    results = classifier.predict(path)

    # 提取预测标签并转化为逗号分隔的字符串
    tags = ', '.join([label for label, confidence in results])

    return tags
# import tempfile
# import os
# import requests
# from io import BytesIO
# from PIL import Image as PILImage
# from .models import Image
# from image_classifier import ImageClassifier  # 引入你的分类器
# import logging
#
# logger = logging.getLogger(__name__)
#
# def ai_image_analysis(image_id):
#     try:
#         # 获取图像对象
#         image = Image.objects.get(id=image_id)
#
#         # 获取图像 URL
#         image_url = image.image_url
#         logger.info(f"Downloading image from URL: {image_url}")
#
#         # 下载图像
#         response = requests.get(image_url)
#         if response.status_code == 200:
#             # 使用 BytesIO 将图像加载为二进制数据
#             img_data = BytesIO(response.content)
#
#             # 创建临时文件来存储图像
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
#                 temp_file.write(img_data.getvalue())
#                 temp_file_path = temp_file.name  # 临时文件路径
#
#             # 初始化图像分类器
#             classifier = ImageClassifier()
#
#             # 使用分类器进行图像预测（传递临时文件路径）
#             results = classifier.predict(temp_file_path)
#
#             # 提取预测标签
#             tags = [label for label, confidence in results]
#
#             # 更新图像的 tags 字段
#             image.tags = ', '.join(tags)
#             image.save()
#
#             # 删除临时文件
#             os.remove(temp_file_path)
#
#             # 返回成功
#             return f"AI analysis completed for image {image_id}. Tags: {tags}"
#
#         else:
#             logger.error(f"Failed to download image from URL {image_url}. Status code: {response.status_code}")
#             return f"Failed to download image from URL {image_url}. Status code: {response.status_code}"
#
#     except Image.DoesNotExist:
#         logger.error(f"Image with ID {image_id} not found.")
#         return f"Image with ID {image_id} not found."
#     except Exception as e:
#         logger.error(f"An error occurred while processing image {image_id}: {str(e)}")
#         return f"An error occurred: {str(e)}"



