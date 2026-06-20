import cv2
import numpy as np

IMG_HEIGHT = 150
IMG_WIDTH = 150

def resize_keep_aspect_ration(img, target_height=IMG_HEIGHT, target_width=IMG_WIDTH, pad_value=255):
    aspect_ratio = img.shape[1] / img.shape[0]

    if aspect_ratio > target_width / target_height:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    resized_img = cv2.resize(img, (new_width, new_height))

    preprocessed_img = np.full((target_height, target_width), pad_value, dtype=np.uint8)
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    preprocessed_img[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_img

    return preprocessed_img

def preprocess_image(img_dir):
    img = cv2.imread(img_dir, cv2.IMREAD_GRAYSCALE)
    img = resize_keep_aspect_ration(img)
    img = img / 255.0
    return img

def calculate_image_size_and_aspect_ratio(df):
    image_sizes = []
    aspect_ratios = []

    for image_path in df['ImagePath']:
        image = PIL.Image.open(image_path)
        width, height = image.size
        image_sizes.append(width * height)
        aspect_ratios.append(width / height)
    return image_sizes, aspect_ratios