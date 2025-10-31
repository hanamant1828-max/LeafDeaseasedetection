#!/usr/bin/env python3
"""
Download plant disease images from Kaggle and organize them into training folders.
Uses memory-efficient streaming extraction to avoid OOM errors.
"""
import os
import shutil
import random
import zipfile
import tempfile
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

# Configuration
DATASET = 'rashikrahmanpritom/plant-disease-recognition-dataset'
TARGET_HEALTHY_DIR = './training_data/healthy'
TARGET_DISEASED_DIR = './training_data/diseased'
NUM_HEALTHY = 500
NUM_DISEASED = 500

def main():
    # Initialize Kaggle API
    api = KaggleApi()
    api.authenticate()
    
    # Create target directories
    os.makedirs(TARGET_HEALTHY_DIR, exist_ok=True)
    os.makedirs(TARGET_DISEASED_DIR, exist_ok=True)
    
    print(f"Downloading: {DATASET}")
    print("="*60)
    
    # Use temp directory for download
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory: {temp_dir}")
        
        # Download dataset
        print("\nStep 1: Downloading ZIP file...")
        api.dataset_download_files(DATASET, path=temp_dir, unzip=False)
        
        # Find the ZIP file
        zip_files = [f for f in os.listdir(temp_dir) if f.endswith('.zip')]
        if not zip_files:
            print("❌ No ZIP file found!")
            return
        
        zip_path = os.path.join(temp_dir, zip_files[0])
        zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"✓ Downloaded: {zip_files[0]} ({zip_size_mb:.1f} MB)")
        
        # Process ZIP file
        print("\nStep 2: Scanning ZIP contents...")
        healthy_images = []
        diseased_images = []
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            all_files = [f for f in zf.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png')) 
                        and not f.startswith('__MACOSX') and not os.path.basename(f).startswith('.')]
            
            print(f"Total images found: {len(all_files)}")
            
            # Categorize
            for filepath in all_files:
                path_lower = filepath.lower()
                if 'healthy' in path_lower:
                    healthy_images.append(filepath)
                else:
                    # Anything not healthy is considered diseased
                    diseased_images.append(filepath)
            
            print(f"  Healthy: {len(healthy_images)}")
            print(f"  Diseased: {len(diseased_images)}")
            
            # Sample images
            sample_healthy = random.sample(healthy_images, min(NUM_HEALTHY, len(healthy_images)))
            sample_diseased = random.sample(diseased_images, min(NUM_DISEASED, len(diseased_images)))
            
            # Extract healthy images
            print(f"\nStep 3: Extracting {len(sample_healthy)} healthy images...")
            for idx, filepath in enumerate(sample_healthy, 1):
                try:
                    ext = os.path.splitext(filepath)[1] or '.jpg'
                    target = os.path.join(TARGET_HEALTHY_DIR, f'healthy_{idx:04d}{ext}')
                    
                    with zf.open(filepath) as source, open(target, 'wb') as dest:
                        shutil.copyfileobj(source, dest)
                    
                    if idx % 100 == 0:
                        print(f"  ✓ {idx}/{len(sample_healthy)}")
                except Exception as e:
                    print(f"  ⚠ Error extracting {filepath}: {e}")
            
            # Extract diseased images
            print(f"\nStep 4: Extracting {len(sample_diseased)} diseased images...")
            for idx, filepath in enumerate(sample_diseased, 1):
                try:
                    ext = os.path.splitext(filepath)[1] or '.jpg'
                    target = os.path.join(TARGET_DISEASED_DIR, f'diseased_{idx:04d}{ext}')
                    
                    with zf.open(filepath) as source, open(target, 'wb') as dest:
                        shutil.copyfileobj(source, dest)
                    
                    if idx % 100 == 0:
                        print(f"  ✓ {idx}/{len(sample_diseased)}")
                except Exception as e:
                    print(f"  ⚠ Error extracting {filepath}: {e}")
    
    # Count final results
    actual_healthy = len([f for f in os.listdir(TARGET_HEALTHY_DIR) if not f.startswith('.')])
    actual_diseased = len([f for f in os.listdir(TARGET_DISEASED_DIR) if not f.startswith('.')])
    
    print("\n" + "="*60)
    print("✓ SUCCESS!")
    print("="*60)
    print(f"✓ {actual_healthy} healthy images → {TARGET_HEALTHY_DIR}")
    print(f"✓ {actual_diseased} diseased images → {TARGET_DISEASED_DIR}")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
