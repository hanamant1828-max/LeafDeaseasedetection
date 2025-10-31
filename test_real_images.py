#!/usr/bin/env python3
"""
Test model with real test images
"""
import os
import numpy as np
from PIL import Image
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('models/plant_disease_model.keras')
print("Model loaded successfully\n")

# Test on actual test images
test_images = []

# Add healthy test images
healthy_dir = 'test_images/healthy'
if os.path.exists(healthy_dir):
    for fname in os.listdir(healthy_dir):
        if fname.endswith(('.png', '.jpg', '.jpeg')):
            test_images.append((os.path.join(healthy_dir, fname), 'healthy'))

# Add diseased test images
diseased_dir = 'test_images/diseased'
if os.path.exists(diseased_dir):
    for fname in os.listdir(diseased_dir):
        if fname.endswith(('.png', '.jpg', '.jpeg')):
            test_images.append((os.path.join(diseased_dir, fname), 'diseased'))

print("="*80)
print("TESTING WITH REAL TEST IMAGES")
print("="*80)

correct = 0
total = 0

for img_path, expected_label in sorted(test_images):
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
    
    is_correct = predicted_label == expected_label
    if is_correct:
        correct += 1
    total += 1
    
    match = "✓" if is_correct else "✗"
    
    print(f"\n{match} {os.path.basename(img_path)}")
    print(f"  Expected: {expected_label}")
    print(f"  Predicted: {predicted_label} ({confidence:.1f}% confidence)")
    print(f"  Raw prediction value: {prediction:.6f}")

print("\n" + "="*80)
print(f"ACCURACY: {correct}/{total} ({100*correct/total:.1f}%)")
print("="*80)
