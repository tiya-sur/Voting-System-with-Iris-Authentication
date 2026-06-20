import numpy as np

def extract_features(segmented_iris):
    try:
        features = segmented_iris.flatten() 
        return features
    except:
        return None