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
EPOCHS = 10  # Reduced from 15
LEARNING_RATE = 0.001  # Slightly higher for faster convergence

os.makedirs('models', exist_ok=True)

print(f"\n=== Quick Plant Disease Model Training ===")
print(f"Training data directory: {TRAIN_DATA_DIR}")
print(f"Image size: {IMAGE_SIZE}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Epochs: {EPOCHS}")

# Simpler data augmentation for faster training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
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

print("\n=== Building Model ===")
base_model = MobileNetV2(
    input_shape=IMAGE_SIZE + (3,),
    include_top=False,
    weights='imagenet'
)

# Keep base frozen
base_model.trainable = False

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
    metrics=['accuracy', keras.metrics.AUC(name='auc')]
)

print("\n=== Model Architecture ===")
model.summary()

print("\n=== Training Model ===")
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True,
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
    callbacks=[early_stopping, checkpoint],
    verbose=1
)

print("\n=== Training Complete ===")
print(f"Model saved to: {MODEL_SAVE_PATH}")

# Evaluate
print("\n=== Final Evaluation ===")
val_loss, val_accuracy, val_auc = model.evaluate(validation_generator, verbose=0)
print(f"Validation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {val_accuracy:.4f}")
print(f"Validation AUC: {val_auc:.4f}")
