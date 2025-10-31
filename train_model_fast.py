import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

print("TensorFlow version:", tf.__version__)

TRAIN_DATA_DIR = 'training_data'
MODEL_SAVE_PATH = 'models/plant_disease_model.keras'
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 16
EPOCHS = 10

os.makedirs('models', exist_ok=True)

print(f"\n=== Plant Disease Detection Model Training (Fast Version) ===")
print(f"Training data: {TRAIN_DATA_DIR}")
print(f"Image size: {IMAGE_SIZE}")
print(f"Epochs: {EPOCHS}")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    horizontal_flip=True,
    validation_split=0.2
)

print("\n=== Loading Data ===")
train_gen = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

val_gen = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

print(f"Training: {train_gen.samples} images")
print(f"Validation: {val_gen.samples} images")
print(f"Classes: {train_gen.class_indices}")

print("\n=== Building Lightweight CNN ===")
model = keras.Sequential([
    layers.Input(shape=IMAGE_SIZE + (3,)),
    
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(2),
    layers.BatchNormalization(),
    
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(2),
    layers.BatchNormalization(),
    
    layers.Conv2D(128, 3, activation='relu'),
    layers.MaxPooling2D(2),
    layers.BatchNormalization(),
    
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

print("\n=== Training ===")
history = model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen,
    verbose=2
)

model.save(MODEL_SAVE_PATH)
print(f"\n=== Model saved to {MODEL_SAVE_PATH} ===")

final_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]
print(f"Training Accuracy: {final_acc:.4f}")
print(f"Validation Accuracy: {final_val_acc:.4f}")

with open('models/class_indices.txt', 'w') as f:
    for cls_name, cls_idx in train_gen.class_indices.items():
        f.write(f"{cls_name}:{cls_idx}\n")
print("Class indices saved")

print("\n=== Done! ===")
