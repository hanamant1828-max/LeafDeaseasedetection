#!/usr/bin/env python3
"""
Test model accuracy on sample images
"""
import os
import numpy as np
from PIL import Image
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('models/plant_disease_model.keras')
print("Model loaded successfully")
print(f"Input shape: {model.input_shape}")
print(f"Output shape: {model.output_shape}")

# Test on some training images to verify the model behavior
test_images = [
    ('training_data/healthy/healthy_0001.jpg', 'healthy'),
    ('training_data/healthy/healthy_0002.jpg', 'healthy'),
    ('training_data/healthy/healthy_0003.jpg', 'healthy'),
    ('training_data/diseased/diseased_0001.jpg', 'diseased'),
    ('training_data/diseased/diseased_0002.jpg', 'diseased'),
    ('training_data/diseased/diseased_0003.jpg', 'diseased'),
]

print("\n" + "="*80)
print("TESTING MODEL PREDICTIONS")
print("="*80)

for img_path, expected_label in test_images:
    if not os.path.exists(img_path):
        print(f"\nSkipping {img_path} - file not found")
        continue
    
    # Load and preprocess image
    img = Image.open(img_path).convert('RGB')
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Get prediction
    prediction = model.predict(img_array, verbose=0)[0][0]
    
    # Apply same logic as in analysis.py
    if prediction > 0.5:
        predicted_label = 'healthy'
        confidence = float(prediction * 100)
    else:
        predicted_label = 'diseased'
        confidence = float((1 - prediction) * 100)
    
    match = "✓" if predicted_label == expected_label else "✗"
    
    print(f"\n{match} {os.path.basename(img_path)}")
    print(f"  Expected: {expected_label}")
    print(f"  Predicted: {predicted_label} ({confidence:.1f}% confidence)")
    print(f"  Raw prediction value: {prediction:.6f}")

print("\n" + "="*80)
