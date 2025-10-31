#!/usr/bin/env python3
"""
Retrain model with improved data augmentation for real-world images
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

print("TensorFlow version:", tf.__version__)

TRAIN_DATA_DIR = 'training_data'
MODEL_SAVE_PATH = 'models/plant_disease_model.keras'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.0001

os.makedirs('models', exist_ok=True)

print(f"\n=== Improved Plant Disease Detection Model Training ===")
print(f"Training data directory: {TRAIN_DATA_DIR}")
print(f"Image size: {IMAGE_SIZE}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Epochs: {EPOCHS}")

# Enhanced data augmentation to simulate real-world conditions
train_datagen = ImageDataGenerator(
    rescale=1./255,
    # Rotation and flipping
    rotation_range=40,
    horizontal_flip=True,
    vertical_flip=True,
    # Position shifts (simulates different camera angles)
    width_shift_range=0.3,
    height_shift_range=0.3,
    # Zoom (simulates different distances)
    zoom_range=[0.5, 1.5],  # Can zoom out significantly (full plant) or in (close-up)
    # Shear and fill
    shear_range=0.3,
    fill_mode='reflect',
    # Brightness and contrast variations (simulates different lighting)
    brightness_range=[0.5, 1.5],
    # Channel shifts (simulates different camera color profiles)
    channel_shift_range=30.0,
    # Validation split
    validation_split=0.2
)

print("\n=== Loading Training Data ===")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training',
    shuffle=True,
    seed=42
)

print("\n=== Loading Validation Data ===")
validation_generator = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation',
    shuffle=True,
    seed=42
)

print(f"\nFound {train_generator.samples} training images")
print(f"Found {validation_generator.samples} validation images")
print(f"Classes: {train_generator.class_indices}")

print("\n=== Building Improved Model ===")
base_model = MobileNetV2(
    input_shape=IMAGE_SIZE + (3,),
    include_top=False,
    weights='imagenet'
)

# Fine-tune more layers for better generalization
base_model.trainable = True
for layer in base_model.layers[:-50]:  # Freeze only bottom layers
    layer.trainable = False

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.4),  # Increased dropout to prevent overfitting
    layers.Dense(256, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='binary_crossentropy',
    metrics=['accuracy', keras.metrics.AUC(name='auc'), 
             keras.metrics.Precision(name='precision'),
             keras.metrics.Recall(name='recall')]
)

print("\n=== Model Architecture ===")
model.summary()

print("\n=== Training Model ===")
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=7,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=4,
    min_lr=1e-7,
    verbose=1
)

checkpoint = keras.callbacks.ModelCheckpoint(
    MODEL_SAVE_PATH,
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=[early_stopping, reduce_lr, checkpoint],
    verbose=1
)

model.save(MODEL_SAVE_PATH)
print(f"\n=== Model saved to {MODEL_SAVE_PATH} ===")

# Print final metrics
final_train_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]
final_train_auc = history.history['auc'][-1]
final_val_auc = history.history['val_auc'][-1]

print("\n=== Training Results ===")
print(f"Final Training Accuracy: {final_train_acc:.4f}")
print(f"Final Validation Accuracy: {final_val_acc:.4f}")
print(f"Final Training AUC: {final_train_auc:.4f}")
print(f"Final Validation AUC: {final_val_auc:.4f}")

print("\n=== Training Complete! ===")
print("The model now handles real-world images with various:")
print("  - Zoom levels (close-up leaves to full plants)")
print("  - Lighting conditions (bright, dim, shadows)")
print("  - Camera angles and positions")
print("  - Color variations from different cameras")
