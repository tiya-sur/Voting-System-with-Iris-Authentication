# iris_segmentation.py (Combined with feature extraction)
import numpy as np
import tensorflow as tf
from keras.models import load_model
import cv2
import cv2

MODEL_PATH = "IRISRecognizer.h5"  # Path to your trained model

def extract_features(image_path):
    
    try:
        model = load_model(MODEL_PATH)
        feature_extractor = tf.keras.Model(inputs=model.inputs, outputs=model.get_layer("Mpool7").output) 

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return None

       
        img = resize_keep_aspect_ration(image)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        features = feature_extractor.predict(img)
        return features.flatten()

    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def resize_keep_aspect_ration(img, target_height=150, target_width=150, pad_value=255):
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



def segment_iris(image):
    try:
        image = cv2.resize(image, (320, 240)) 
        cv2.imshow("Segmented Iris", image) 
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return image
    except:
        return None