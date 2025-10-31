import os
import shutil
import random
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

# Configuration
DATASET = 'vipoooool/new-plant-diseases-dataset'
DOWNLOAD_PATH = './temp_download'
TARGET_HEALTHY_DIR = './training_data/healthy'
TARGET_DISEASED_DIR = './training_data/diseased'
NUM_HEALTHY = 500
NUM_DISEASED = 500

# Create target directories
os.makedirs(TARGET_HEALTHY_DIR, exist_ok=True)
os.makedirs(TARGET_DISEASED_DIR, exist_ok=True)

print("Downloading dataset (this may take a while)...")
try:
    # Download the dataset
    api.dataset_download_files(DATASET, path=DOWNLOAD_PATH, unzip=True)
    print("Download complete!")
    
    # Find all healthy and diseased images
    healthy_images = []
    diseased_images = []
    
    # Walk through the downloaded directory
    for root, dirs, files in os.walk(DOWNLOAD_PATH):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(root, file)
                # Check if it's a healthy image (contains 'healthy' in path)
                if 'healthy' in root.lower() or 'healthy' in file.lower():
                    healthy_images.append(filepath)
                else:
                    diseased_images.append(filepath)
    
    print(f"\nFound {len(healthy_images)} healthy images")
    print(f"Found {len(diseased_images)} diseased images")
    
    # Randomly select images
    selected_healthy = random.sample(healthy_images, min(NUM_HEALTHY, len(healthy_images)))
    selected_diseased = random.sample(diseased_images, min(NUM_DISEASED, len(diseased_images)))
    
    # Copy healthy images
    print(f"\nCopying {len(selected_healthy)} healthy images...")
    for idx, src in enumerate(selected_healthy, 1):
        ext = os.path.splitext(src)[1]
        dst = os.path.join(TARGET_HEALTHY_DIR, f'healthy_{idx:04d}{ext}')
        shutil.copy2(src, dst)
        if idx % 50 == 0:
            print(f"  Copied {idx}/{len(selected_healthy)} healthy images")
    
    # Copy diseased images
    print(f"\nCopying {len(selected_diseased)} diseased images...")
    for idx, src in enumerate(selected_diseased, 1):
        ext = os.path.splitext(src)[1]
        dst = os.path.join(TARGET_DISEASED_DIR, f'diseased_{idx:04d}{ext}')
        shutil.copy2(src, dst)
        if idx % 50 == 0:
            print(f"  Copied {idx}/{len(selected_diseased)} diseased images")
    
    # Clean up temporary download
    print("\nCleaning up temporary files...")
    shutil.rmtree(DOWNLOAD_PATH)
    
    print("\n✓ Success!")
    print(f"✓ {len(selected_healthy)} healthy images saved to: {TARGET_HEALTHY_DIR}")
    print(f"✓ {len(selected_diseased)} diseased images saved to: {TARGET_DISEASED_DIR}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    # Clean up on error
    if os.path.exists(DOWNLOAD_PATH):
        shutil.rmtree(DOWNLOAD_PATH)
