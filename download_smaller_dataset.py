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

# Try smaller dataset first
DATASET = 'emmarex/plantdisease'  # PlantVillage dataset - smaller and well organized
ZIP_FILE = './dataset.zip'
TARGET_HEALTHY_DIR = './training_data/healthy'
TARGET_DISEASED_DIR = './training_data/diseased'
NUM_HEALTHY = 500
NUM_DISEASED = 500

# Create target directories
os.makedirs(TARGET_HEALTHY_DIR, exist_ok=True)
os.makedirs(TARGET_DISEASED_DIR, exist_ok=True)

print(f"Downloading dataset: {DATASET}")
print("This is a smaller dataset that should work better...")

try:
    # Download as zip
    api.dataset_download_files(DATASET, path='.', unzip=False)
    
    # Find the downloaded zip file
    zip_files = [f for f in os.listdir('.') if f.endswith('.zip') and os.path.getsize(f) > 1000000]
    if zip_files:
        ZIP_FILE = max(zip_files, key=os.path.getsize)  # Get largest zip
    
    file_size_mb = os.path.getsize(ZIP_FILE) / (1024 * 1024)
    print(f"\nDownloaded: {ZIP_FILE} ({file_size_mb:.1f} MB)")
    
    print("\nScanning ZIP contents...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        all_files = zip_ref.namelist()
        image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.JPG')) 
                      and not f.startswith('__MACOSX') and not f.startswith('.')]
        
        print(f"Total images found: {len(image_files)}")
        
        # Categorize files - look for 'healthy' in filename or path
        healthy_files = []
        diseased_files = []
        
        for f in image_files:
            f_lower = f.lower()
            if 'healthy' in f_lower:
                healthy_files.append(f)
            elif any(disease in f_lower for disease in ['blight', 'spot', 'rust', 'scab', 'mold', 'mildew', 
                                                          'leaf', 'bacterial', 'fungal', 'virus', 'disease',
                                                          'early', 'late', 'septoria', 'target', 'cercospora']):
                diseased_files.append(f)
        
        print(f"Healthy images: {len(healthy_files)}")
        print(f"Diseased images: {len(diseased_files)}")
        
        if len(healthy_files) == 0 or len(diseased_files) == 0:
            print("\n⚠ Warning: Not enough categorized images found.")
            print("Sampling from all images...")
            # If categorization failed, take random split
            random.shuffle(image_files)
            split_point = len(image_files) // 2
            healthy_files = image_files[:split_point]
            diseased_files = image_files[split_point:]
        
        # Select random subset
        num_healthy_to_extract = min(NUM_HEALTHY, len(healthy_files))
        num_diseased_to_extract = min(NUM_DISEASED, len(diseased_files))
        
        selected_healthy = random.sample(healthy_files, num_healthy_to_extract)
        selected_diseased = random.sample(diseased_files, num_diseased_to_extract)
        
        print(f"\nExtracting {num_healthy_to_extract} healthy images...")
        for idx, filename in enumerate(selected_healthy, 1):
            try:
                source = zip_ref.open(filename)
                ext = os.path.splitext(filename)[1] or '.jpg'
                target = os.path.join(TARGET_HEALTHY_DIR, f'healthy_{idx:04d}{ext}')
                
                with open(target, 'wb') as target_file:
                    shutil.copyfileobj(source, target_file)
                
                if idx % 100 == 0:
                    print(f"  {idx}/{num_healthy_to_extract} healthy images")
            except Exception as e:
                print(f"  ⚠ Skipped {filename}: {e}")
        
        print(f"\nExtracting {num_diseased_to_extract} diseased images...")
        for idx, filename in enumerate(selected_diseased, 1):
            try:
                source = zip_ref.open(filename)
                ext = os.path.splitext(filename)[1] or '.jpg'
                target = os.path.join(TARGET_DISEASED_DIR, f'diseased_{idx:04d}{ext}')
                
                with open(target, 'wb') as target_file:
                    shutil.copyfileobj(source, target_file)
                
                if idx % 100 == 0:
                    print(f"  {idx}/{num_diseased_to_extract} diseased images")
            except Exception as e:
                print(f"  ⚠ Skipped {filename}: {e}")
    
    # Clean up zip file
    print("\nCleaning up...")
    os.remove(ZIP_FILE)
    
    # Count actual extracted files
    actual_healthy = len(os.listdir(TARGET_HEALTHY_DIR))
    actual_diseased = len(os.listdir(TARGET_DISEASED_DIR))
    
    print("\n" + "="*60)
    print("✓ SUCCESS!")
    print("="*60)
    print(f"✓ {actual_healthy} healthy images → {TARGET_HEALTHY_DIR}")
    print(f"✓ {actual_diseased} diseased images → {TARGET_DISEASED_DIR}")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    # Clean up on error
    for f in os.listdir('.'):
        if f.endswith('.zip'):
            try:
                os.remove(f)
            except:
                pass
