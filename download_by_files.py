#!/usr/bin/env python3
import os
import random
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

DATASET = 'abdallahalidev/plantvillage-dataset'
TARGET_HEALTHY_DIR = './training_data/healthy'
TARGET_DISEASED_DIR = './training_data/diseased'
NUM_HEALTHY = 500
NUM_DISEASED = 500

# Create target directories
os.makedirs(TARGET_HEALTHY_DIR, exist_ok=True)
os.makedirs(TARGET_DISEASED_DIR, exist_ok=True)

print(f"Fetching file list from: {DATASET}")
files = api.dataset_list_files(DATASET).files

# Categorize files
healthy_files = []
diseased_files = []

print("Categorizing images...")
for f in files:
    name_lower = f.name.lower()
    if 'healthy' in name_lower:
        healthy_files.append(f.name)
    elif any(disease in name_lower for disease in ['scab', 'rot', 'rust', 'blight', 'spot', 'mildew', 'mold', 'wilt']):
        diseased_files.append(f.name)

print(f"Found {len(healthy_files)} healthy images")
print(f"Found {len(diseased_files)} diseased images")

# Sample files to download
num_healthy_download = min(NUM_HEALTHY, len(healthy_files))
num_diseased_download = min(NUM_DISEASED, len(diseased_files))

selected_healthy = random.sample(healthy_files, num_healthy_download)
selected_diseased = random.sample(diseased_files, num_diseased_download)

print(f"\nDownloading {num_healthy_download} healthy images...")
for idx, file_path in enumerate(selected_healthy, 1):
    try:
        # Download file directly
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1] or '.jpg'
        target_path = os.path.join(TARGET_HEALTHY_DIR, f'healthy_{idx:04d}{ext}')
        
        api.dataset_download_file(DATASET, file_path, path=TARGET_HEALTHY_DIR)
        
        # Rename downloaded file
        downloaded = os.path.join(TARGET_HEALTHY_DIR, filename)
        if os.path.exists(downloaded):
            os.rename(downloaded, target_path)
        
        if idx % 50 == 0:
            print(f"  {idx}/{num_healthy_download} healthy images downloaded")
    except Exception as e:
        print(f"  ⚠ Error downloading {file_path}: {e}")

print(f"\nDownloading {num_diseased_download} diseased images...")
for idx, file_path in enumerate(selected_diseased, 1):
    try:
        # Download file directly
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1] or '.jpg'
        target_path = os.path.join(TARGET_DISEASED_DIR, f'diseased_{idx:04d}{ext}')
        
        api.dataset_download_file(DATASET, file_path, path=TARGET_DISEASED_DIR)
        
        # Rename downloaded file
        downloaded = os.path.join(TARGET_DISEASED_DIR, filename)
        if os.path.exists(downloaded):
            os.rename(downloaded, target_path)
        
        if idx % 50 == 0:
            print(f"  {idx}/{num_diseased_download} diseased images downloaded")
    except Exception as e:
        print(f"  ⚠ Error downloading {file_path}: {e}")

# Count actual files
actual_healthy = len([f for f in os.listdir(TARGET_HEALTHY_DIR) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg'))])
actual_diseased = len([f for f in os.listdir(TARGET_DISEASED_DIR) if f.endswith(('.jpg', '.JPG', '.png', '.jpeg'))])

print("\n" + "="*60)
print("✓ DOWNLOAD COMPLETE!")
print("="*60)
print(f"✓ {actual_healthy} healthy images → {TARGET_HEALTHY_DIR}")
print(f"✓ {actual_diseased} diseased images → {TARGET_DISEASED_DIR}")
print("="*60)
