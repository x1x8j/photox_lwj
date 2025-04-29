import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
import requests
from io import BytesIO



class ImageClassifier:
    def __init__(self):

    # 加载模型（使用新版 API）
     self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)  # 或 IMAGENET1K_V2
     self.model.eval()


    def predict(self,image_name):
        # # 检查输入是 URL 还是本地文件路径
        # if image_name.startswith('http://') or image_name.startswith('https://'):
        #     # 从 URL 下载图像
        #     response = requests.get(image_name)
        #     # 二进制数据
        #     image = Image.open(BytesIO(response.content)).convert("RGB")
        # else:
        #     # 从本地文件加载图像
        #     image = Image.open(image_name).convert("RGB")

        # 图像预处理（自动匹配权重对应的预处理）
        preprocess = models.ResNet50_Weights.DEFAULT.transforms()
        image = Image.open(image_name).convert("RGB")
        input_tensor = preprocess(image).unsqueeze(0)

        # 推理

        with torch.no_grad():
             output = self.model(input_tensor)

        # 解析结果
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_probs, top_indices = torch.topk(probabilities, 5)

        # 转换为Python数值
        top_probs = top_probs.cpu().numpy()
        top_indices = top_indices.cpu().numpy()

        # 加载正确的类别文件
        with open("imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]

        # 验证类别数量
        assert len(categories) == 1000, "类别文件必须包含 1000 个类别"
        # 生成结果列表
        results = [
            (categories[idx], float(prob))
            for idx, prob in zip(top_indices, top_probs)
        ]

        return results

