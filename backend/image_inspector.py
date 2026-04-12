from io import BytesIO

import numpy as np
import torch
from PIL import Image
from torchvision import models, transforms


_encoder = None


def load_image_encoder():
    global _encoder
    if _encoder is None:
        model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        _encoder = torch.nn.Sequential(*list(model.children())[:-1])
        _encoder.eval()
    return _encoder


def extract_image_features(image_bytes: bytes) -> dict:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize((256, 256), Image.BILINEAR)
    array = np.asarray(image).astype(np.float32) / 255.0

    grayscale = np.dot(array, [0.2989, 0.5870, 0.1140])
    brightness = float(np.mean(grayscale))
    contrast = float(np.std(grayscale))
    dark_ratio = float(np.mean(grayscale < 0.2))

    gx = np.abs(np.diff(grayscale, axis=1))
    gy = np.abs(np.diff(grayscale, axis=0))
    edges = np.pad(gx, ((0, 0), (0, 1)), mode="constant") + np.pad(gy, ((0, 1), (0, 0)), mode="constant")
    edge_density = float(np.mean(edges > 0.15))

    red_ratio = float(np.mean(array[..., 0]))
    green_ratio = float(np.mean(array[..., 1]))
    blue_ratio = float(np.mean(array[..., 2]))

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        embedding = load_image_encoder()(tensor)
    embedding = embedding.squeeze().numpy()

    return {
        "image_brightness": round(brightness, 4),
        "image_contrast": round(contrast, 4),
        "image_edge_density": round(edge_density, 4),
        "image_dark_ratio": round(dark_ratio, 4),
        "image_red_ratio": round(red_ratio, 4),
        "image_green_ratio": round(green_ratio, 4),
        "image_blue_ratio": round(blue_ratio, 4),
        "image_embedding_mean": round(float(np.mean(embedding)), 4),
        "image_embedding_std": round(float(np.std(embedding)), 4),
        "image_embedding_max": round(float(np.max(embedding)), 4),
        "image_embedding_l2": round(float(np.linalg.norm(embedding)), 4),
    }
