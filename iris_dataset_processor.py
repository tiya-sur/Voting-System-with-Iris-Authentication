# iris_dataset_processor.py
import os
import numpy as np
import tensorflow as tf
from keras import Sequential
from sklearn.preprocessing import LabelEncoder
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from keras.layers import Layer, Input, Dense, Dropout, Conv2D, BatchNormalization, Flatten, MaxPooling2D, GaussianNoise
import cv2
import pandas as pd

# --- Configuration ---
SIZE = 20000
NUM_CLASSES = 2000
IMG_HEIGHT = 150
IMG_WIDTH = 150
NUM_CHANNELS = 1
input_shape = (IMG_HEIGHT, IMG_WIDTH, NUM_CHANNELS)
EPOCHS = 100
BATCH_SIZE = 32
loss = 'sparse_categorical_crossentropy'
activation = "leaky_relu"
initial_learning_rate = 0.001

# --- Data Loading and Exploration ---
def load_dataset(path):
    labels = []
    images = []
    for folder in os.listdir(path):
        for lr in os.listdir(os.path.join(path, folder)):
            for image in os.listdir(os.path.join(path, folder, lr)):
                if not image.endswith('b'):
                    images.append(os.path.join(path, folder, lr, image))
                    labels.append(f"{folder}-{lr}")
    df = pd.DataFrame(list(zip(labels, images)), columns=['Label', 'ImagePath'])
    return df, labels, images

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

def preprocess_labels(df):
    labels = df['Label'].astype(str)
    le = LabelEncoder()
    le.fit(labels)
    labels = le.transform(labels)
    return labels

def split_dataset(preprocessed_images, preprocessed_labels, train_size=0.8, validation_size=0.1, shuffle=True):
    np.random.seed(1190652)
    indices = np.arange(SIZE)
    if shuffle:
        np.random.shuffle(indices)
    train_samples = int(SIZE * train_size)
    validation_samples = int(SIZE * validation_size)
    train_indices = indices[:train_samples]
    validation_indices = indices[train_samples:train_samples + validation_samples]
    test_indices = indices[train_samples + validation_samples:]
    x_train = preprocessed_images[train_indices]
    y_train = preprocessed_labels[train_indices]
    x_valid = preprocessed_images[validation_indices]
    y_valid = preprocessed_labels[validation_indices]
    x_test = preprocessed_images[test_indices]
    y_test = preprocessed_labels[test_indices]
    return x_train, x_valid, x_test, y_train, y_valid, y_test

def prepare_dataset(df):
    preprocessed_images = []
    for i in range(SIZE):
        image = preprocess_image(images[i])
        preprocessed_images.append(image)
    preprocessed_images = np.array(preprocessed_images).reshape(-1, IMG_HEIGHT, IMG_WIDTH, NUM_CHANNELS)
    preprocessed_labels = preprocess_labels(df)
    return split_dataset(preprocessed_images, preprocessed_labels)

# --- Model ---
class CentralCrop(Layer):
    def __init__(self, central_fraction=0.5):
        super(CentralCrop, self).__init__()
        self.central_fraction = central_fraction

    def call(self, inputs):
        return tf.image.central_crop(inputs, central_fraction=self.central_fraction)

data_augmentation = tf.keras.Sequential([
    Input(shape=input_shape),
    CentralCrop(central_fraction=0.5)
])

def create_model():
    padding = 'same'
    poolpadding = 'valid'
    model = Sequential([
        Input(input_shape),
        Conv2D(32, (5, 5), padding=padding, activation=activation, name="Conv1"),
        BatchNormalization(axis=-1, name="BN1"),
        MaxPooling2D(pool_size=(2, 2), padding=poolpadding, name="Mpool1"),
        GaussianNoise(0.1, name="GaussianNoise"),
        Dropout(0.1, name="Dropout1"),
        Conv2D(64, (5, 5), padding=padding, activation=activation, name="Conv2"),
        BatchNormalization(axis=-1, name="BN2"),
        MaxPooling2D(pool_size=(2, 2), padding=poolpadding, name="Mpool2"),
        Dropout(0.1, name="Dropout2"),
        Conv2D(128, (5, 5), padding=padding, activation=activation, name="Conv3"),
        BatchNormalization(axis=-1, name="BN3"),
        MaxPooling2D(pool_size=(2, 2), padding=poolpadding, name="Mpool3"),
        Dropout(0.25, name="Dropout3"),
        Conv2D(256, (3, 3), padding=padding, activation=activation, name="Conv4"),
        BatchNormalization(axis=-1, name="BN4"),
        MaxPooling2D(pool_size=(2, 2), padding=poolpadding, name="Mpool4"),
        Dropout(0.25, name="Dropout4"),
        Conv2D(256, (3, 3), padding=padding, activation=activation, name="Conv5"),
        BatchNormalization(axis=-1, name="BN5"),
        MaxPooling2D(pool_size=(2, 2), padding=poolpadding, name="Mpool5"),
        Dropout(0.25, name="Dropout5"),
        Conv2D(512, (3, 3), padding=padding, activation=activation, name="Conv6"),
        BatchNormalization(axis=-1, name="BN6"),
        MaxPooling2D(pool_size=(2, 2), padding=poolpadding, name="Mpool6"),
        Dropout(0.45, name="Dropout6"),
        Conv2D(512, (2, 2), padding=padding, activation=activation, name="Conv7"),
        BatchNormalization(axis=-1, name="BN7"),
        MaxPooling2D(pool_size=(2, 2), padding=poolpadding, name="Mpool7"),
        Dropout(0.5, name="Dropout7"),
        Flatten(),
        Dense(128, activation=activation, name="Dense1"),
        Dense(2000, activation='softmax', name="SoftmaxClasses"),
    ], name="IRISRecognizer")
    model.compile(optimizer=Adam(learning_rate=initial_learning_rate), loss=loss, metrics=['accuracy'])
    return model

# --- Model Training and Feature Extraction ---
def extract_cnn_features(model, image):
    feature_extractor = tf.keras.Model(inputs=model.inputs, outputs=model.get_layer("Mpool7").output) # change layer name to the last convolutional layer.
    features = feature_extractor.predict(np.expand_dims(image, axis=0))
    return features.flatten()

def process_iris_dataset(dataset_path):
    df, _, images = load_dataset(dataset_path)
    x_train, x_valid, x_test, y_train, y_valid, y_test = prepare_dataset(df)
    model = create_model()
    earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
    mcp_save = ModelCheckpoint('.mdl_wts.keras', save_best_only=True, monitor='val_loss', mode='min')
    reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, epsilon=1e-4, mode='min')
    model.fit(np.array(x_train), y_train, validation_data=(np.array(x_valid), y_valid), epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[earlyStopping, mcp_save, reduce_lr_loss])

    for index, row in df.iterrows():
        image_path = row['ImagePath']
        label = row['Label']
        image = preprocess_image(image_path)
        features = extract_cnn_features(model, image)
        database_module.store_iris_features(features, label) # use the new database module.

if __name__ == "__main__":
    dataset_path = '"C:\Users\tiya2\OneDrive\Documents\Online-Voting-Systemnew-main\iris_thousands.csv\iris_thousands.csv"' # change to your path.
    process_iris_dataset(dataset_path)