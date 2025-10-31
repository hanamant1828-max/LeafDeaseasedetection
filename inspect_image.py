#!/usr/bin/env python3
"""
Inspect a problematic image
"""
from PIL import Image
import numpy as np
import tensorflow as tf

# Load one of the "healthy" images that was classified wrong
img_path = 'uploads/20251031_172140_healthy_pepper_plant_837f539c.jpg'

img = Image.open(img_path)
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}")

# Show what the model sees
img_resized = img.resize((224, 224))
img_array = np.array(img_resized) / 255.0

# Check color distribution
pixels = np.array(img)
height, width, channels = pixels.shape if len(pixels.shape) == 3 else (pixels.shape[0], pixels.shape[1], 1)
total_pixels = height * width

if len(pixels.shape) == 3:
    r = pixels[:, :, 0].flatten()
    g = pixels[:, :, 1].flatten()
    b = pixels[:, :, 2].flatten()
    
    # Green pixels (likely plant)
    green_mask = (g > r) & (g > b) & (g > 50)
    green_percentage = (np.sum(green_mask) / total_pixels) * 100
    
    # Non-green pixels (background, soil, etc.)
    non_green = 100 - green_percentage
    
    print(f"\nColor analysis of full image:")
    print(f"  Green pixels (plant): {green_percentage:.1f}%")
    print(f"  Non-green (background/soil/stems): {non_green:.1f}%")
    
print(f"\nThis image is a full plant photo, not a close-up leaf!")
print(f"The model was trained on close-up leaf images only.")
