#!/usr/bin/env python3
"""
Prepare improved training dataset by incorporating real-world images from xyz folder
"""
import os
import shutil
from PIL import Image

# Source directories
XYZ_DIR = 'xyz'
TRAIN_DIR = 'training_data'

# Get all files from xyz
xyz_files = [f for f in os.listdir(XYZ_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]

print("="*80)
print("PREPARING IMPROVED TRAINING DATASET")
print("="*80)

# Categorize xyz images
healthy_images = [f for f in xyz_files if f.startswith('healthy_')]
diseased_images = [f for f in xyz_files if not f.startswith('healthy_')]

print(f"\nReal-world images in xyz folder:")
print(f"  Healthy: {len(healthy_images)}")
print(f"  Diseased: {len(diseased_images)}")

# Count existing training images
existing_healthy = len([f for f in os.listdir(os.path.join(TRAIN_DIR, 'healthy')) if f.endswith(('.jpg', '.png'))])
existing_diseased = len([f for f in os.listdir(os.path.join(TRAIN_DIR, 'diseased')) if f.endswith(('.jpg', '.png'))])

print(f"\nExisting training images:")
print(f"  Healthy: {existing_healthy}")
print(f"  Diseased: {existing_diseased}")

# Copy real-world images to training data
print(f"\nAdding real-world images to training dataset...")

copied_healthy = 0
copied_diseased = 0

for filename in healthy_images:
    src = os.path.join(XYZ_DIR, filename)
    dst = os.path.join(TRAIN_DIR, 'healthy', f'realworld_{filename}')
    
    # Check if already exists
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        copied_healthy += 1

for filename in diseased_images:
    src = os.path.join(XYZ_DIR, filename)
    dst = os.path.join(TRAIN_DIR, 'diseased', f'realworld_{filename}')
    
    # Check if already exists
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        copied_diseased += 1

print(f"\nCopied to training data:")
print(f"  Healthy: {copied_healthy} new images")
print(f"  Diseased: {copied_diseased} new images")

# Final counts
final_healthy = len([f for f in os.listdir(os.path.join(TRAIN_DIR, 'healthy')) if f.endswith(('.jpg', '.png'))])
final_diseased = len([f for f in os.listdir(os.path.join(TRAIN_DIR, 'diseased')) if f.endswith(('.jpg', '.png'))])

print(f"\nFinal training dataset:")
print(f"  Healthy: {final_healthy} images")
print(f"  Diseased: {final_diseased} images")
print(f"  Total: {final_healthy + final_diseased} images")

print(f"\n✓ Dataset prepared successfully!")
print("="*80)
