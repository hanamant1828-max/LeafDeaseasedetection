
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

print("="*70)
print("RETRAINING MODEL WITH VERIFIED LABELS")
print("="*70)

TRAIN_DATA_DIR = 'training_data'
MODEL_SAVE_PATH = 'models/plant_disease_model.keras'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

os.makedirs('models', exist_ok=True)

# Setup data generators
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

print(f"\nTraining samples: {train_generator.samples}")
print(f"Validation samples: {validation_generator.samples}")
print(f"\n*** CLASS MAPPING (CRITICAL) ***")
print(f"Class indices: {train_generator.class_indices}")
print("This means:")
for class_name, class_idx in train_generator.class_indices.items():
    print(f"  - {class_name.upper()} = {class_idx}")
print("*** Model will output values close to these indices ***\n")

# Build model
print("=== Building Model ===")
base_model = MobileNetV2(
    input_shape=IMAGE_SIZE + (3,),
    include_top=False,
    weights='imagenet'
)
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
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy', keras.metrics.AUC(name='auc')]
)

# Train
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

# Save model
model.save(MODEL_SAVE_PATH)
print(f"\n=== Model saved to {MODEL_SAVE_PATH} ===")

# Evaluate
val_loss, val_accuracy, val_auc = model.evaluate(validation_generator, verbose=0)
print("\n=== Final Evaluation ===")
print(f"Validation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {val_accuracy:.4f}")
print(f"Validation AUC: {val_auc:.4f}")

# Save class mapping
with open('models/class_mapping.txt', 'w') as f:
    f.write("CLASS MAPPING FOR MODEL:\n")
    f.write("="*50 + "\n")
    for class_name, class_idx in train_generator.class_indices.items():
        f.write(f"{class_name} = {class_idx}\n")
    f.write("\nPREDICTION INTERPRETATION:\n")
    f.write("="*50 + "\n")
    f.write("Model output close to 0 = diseased\n")
    f.write("Model output close to 1 = healthy\n")
    f.write("\nCODE LOGIC:\n")
    f.write("if prediction > 0.5: disease = 'healthy'\n")
    f.write("else: disease = 'diseased'\n")

print("\n=== Class mapping saved to models/class_mapping.txt ===")
print("\n=== TRAINING COMPLETE ===")
