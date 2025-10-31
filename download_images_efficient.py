#!/usr/bin/env python3
import os
import shutil
import random
import zipfile
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

# Configuration
DATASET = 'vipoooool/new-plant-diseases-dataset'
ZIP_FILE = './dataset.zip'
EXTRACT_PATH = './temp_extract'
TARGET_HEALTHY_DIR = './training_data/healthy'
TARGET_DISEASED_DIR = './training_data/diseased'
NUM_HEALTHY = 500
NUM_DISEASED = 500

# Create target directories
os.makedirs(TARGET_HEALTHY_DIR, exist_ok=True)
os.makedirs(TARGET_DISEASED_DIR, exist_ok=True)

print("Step 1: Downloading dataset as ZIP file...")
try:
    # Download as zip without extracting
    api.dataset_download_files(DATASET, path='.', unzip=False)
    
    # Find the downloaded zip file
    zip_files = [f for f in os.listdir('.') if f.endswith('.zip') and 'plant' in f.lower()]
    if zip_files:
        ZIP_FILE = zip_files[0]
    
    print(f"Downloaded: {ZIP_FILE}")
    
    # Open zip file and read contents
    print("\nStep 2: Scanning ZIP contents...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        all_files = zip_ref.namelist()
        image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.startswith('__MACOSX')]
        
        print(f"Total images found: {len(image_files)}")
        
        # Categorize files
        healthy_files = [f for f in image_files if 'healthy' in f.lower()]
        diseased_files = [f for f in image_files if 'healthy' not in f.lower() and any(x in f.lower() for x in ['blight', 'spot', 'mildew', 'rust', 'scab', 'mold', 'disease'])]
        
        print(f"Healthy images: {len(healthy_files)}")
        print(f"Diseased images: {len(diseased_files)}")
        
        # Select random subset
        selected_healthy = random.sample(healthy_files, min(NUM_HEALTHY, len(healthy_files)))
        selected_diseased = random.sample(diseased_files, min(NUM_DISEASED, len(diseased_files)))
        
        print(f"\nStep 3: Extracting {len(selected_healthy)} healthy images...")
        for idx, filename in enumerate(selected_healthy, 1):
            # Extract directly to target
            source = zip_ref.open(filename)
            ext = os.path.splitext(filename)[1]
            target = os.path.join(TARGET_HEALTHY_DIR, f'healthy_{idx:04d}{ext}')
            
            with open(target, 'wb') as target_file:
                shutil.copyfileobj(source, target_file)
            
            if idx % 100 == 0:
                print(f"  Extracted {idx}/{len(selected_healthy)} healthy images")
        
        print(f"\nStep 4: Extracting {len(selected_diseased)} diseased images...")
        for idx, filename in enumerate(selected_diseased, 1):
            # Extract directly to target
            source = zip_ref.open(filename)
            ext = os.path.splitext(filename)[1]
            target = os.path.join(TARGET_DISEASED_DIR, f'diseased_{idx:04d}{ext}')
            
            with open(target, 'wb') as target_file:
                shutil.copyfileobj(source, target_file)
            
            if idx % 100 == 0:
                print(f"  Extracted {idx}/{len(selected_diseased)} diseased images")
    
    # Clean up zip file
    print("\nStep 5: Cleaning up...")
    os.remove(ZIP_FILE)
    
    print("\n" + "="*60)
    print("✓ SUCCESS!")
    print("="*60)
    print(f"✓ {len(selected_healthy)} healthy images → {TARGET_HEALTHY_DIR}")
    print(f"✓ {len(selected_diseased)} diseased images → {TARGET_DISEASED_DIR}")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    # Clean up on error
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)
    if os.path.exists(EXTRACT_PATH):
        shutil.rmtree(EXTRACT_PATH)
