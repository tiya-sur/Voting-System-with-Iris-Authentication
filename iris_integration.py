'''import cv2
import numpy as np
import iris_segmentation
import iris_feature_extraction
import iris_matching
import database_module

def verify_iris(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return False, "Error: Could not load image."
        segmented_iris = iris_segmentation.segment_iris(image)
        if segmented_iris is None:
            return False, "Error: Iris segmentation failed."
        features = iris_feature_extraction.extract_features(segmented_iris)
        if features is None:
            return False, "Error: Feature extraction failed."
        match_result, message = database_module.match_iris_template(features)
        return match_result, message
    except Exception as e:
        return False, f"Error: An unexpected error occurred: {e}"'''

import cv2
import numpy as np
import iris_segmentation
import iris_feature_extraction
import iris_matching
import database_module

def verify_iris(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return False, "Error: Could not load image."
        segmented_iris = iris_segmentation.segment_iris(image)
        if segmented_iris is None:
            return False, "Error: Iris segmentation failed."
        features = iris_feature_extraction.extract_features(segmented_iris)
        if features is None:
            return False, "Error: Feature extraction failed."
        match_result, message = database_module.match_iris_template(features)
        return match_result, message
    except Exception as e:
        return False, f"Error: An unexpected error occurred: {e}"
