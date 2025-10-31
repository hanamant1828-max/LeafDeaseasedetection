#!/usr/bin/env python3
"""
CORRECTED training with proper validation (NO augmentation on validation set)
"""
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

print("="*80)
print("FINAL CORRECT MODEL TRAINING - PROPER VALIDATION")
print("="*80)

TRAIN_DATA_DIR = 'training_data'
MODEL_SAVE_PATH = 'models/plant_disease_model.keras'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15
LEARNING_RATE = 0.001

# TRAINING generator with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    horizontal_flip=True,
    vertical_flip=True,
    width_shift_range=0.25,
    height_shift_range=0.25,
    zoom_range=0.25,
    brightness_range=[0.7, 1.3],
    shear_range=0.2,
    fill_mode='nearest',
    validation_split=0.2
)

# VALIDATION generator - ONLY rescaling, NO augmentation!
validation_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

print("\nLoading training data (WITH augmentation)...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training',
    shuffle=True,
    seed=42
)

print("Loading validation data (NO augmentation)...")
validation_generator = validation_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation',
    shuffle=False,  # Don't shuffle validation for consistency
    seed=42
)

print(f"\nTraining: {train_generator.samples} images (augmented)")
print(f"Validation: {validation_generator.samples} images (clean, no augmentation)")
print(f"Classes: {train_generator.class_indices}\n")

# Build model
base_model = MobileNetV2(
    input_shape=IMAGE_SIZE + (3,),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='binary_crossentropy',
    metrics=['accuracy', keras.metrics.Precision(name='precision'), 
             keras.metrics.Recall(name='recall')]
)

print("Training model with PROPER validation...\n")

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,  # Uses non-augmented validation generator
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss', 
            patience=5, 
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            MODEL_SAVE_PATH, 
            monitor='val_accuracy', 
            save_best_only=True, 
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', 
            factor=0.5, 
            patience=3, 
            min_lr=1e-6,
            verbose=1
        )
    ],
    verbose=1
)

model.save(MODEL_SAVE_PATH)

print(f"\n{'='*80}")
print(f"TRAINING COMPLETE - TRUSTWORTHY METRICS")
print(f"{'='*80}")
print(f"Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")
print(f"Final Training Precision: {history.history['precision'][-1]:.4f}")
print(f"Final Validation Precision: {history.history['val_precision'][-1]:.4f}")
print(f"Final Training Recall: {history.history['recall'][-1]:.4f}")
print(f"Final Validation Recall: {history.history['val_recall'][-1]:.4f}")
print(f"{'='*80}")
print(f"\n✓ Model saved: {MODEL_SAVE_PATH}")
print("✓ Validation was performed on CLEAN, non-augmented images")
print("✓ Metrics are now TRUSTWORTHY\n")
