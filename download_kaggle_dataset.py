
import os
import zipfile
import shutil
from pathlib import Path

print("=" * 60)
print("PlantVillage Dataset Downloader")
print("=" * 60)

# Check if Kaggle credentials exist
kaggle_dir = Path.home() / '.kaggle'
kaggle_json = kaggle_dir / 'kaggle.json'

if not kaggle_json.exists():
    print("\n⚠️  Kaggle API credentials not found!")
    print("\nTo download from Kaggle, you need to:")
    print("1. Go to https://www.kaggle.com/account")
    print("2. Scroll to 'API' section and click 'Create New Token'")
    print("3. This will download 'kaggle.json' file")
    print("4. Upload kaggle.json to this repl")
    print("5. Run this script again")
    exit(1)

# Set permissions for kaggle.json
os.chmod(kaggle_json, 0o600)

print("\n✓ Kaggle credentials found!")
print("\nDownloading PlantVillage dataset...")
print("This may take several minutes...\n")

# Download the dataset
os.system('kaggle datasets download -d abdallahalidev/plantvillage-dataset -p .')

# Extract the dataset
print("\nExtracting dataset...")
zip_file = 'plantvillage-dataset.zip'

if os.path.exists(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('plantvillage_temp')
    
    print("✓ Dataset extracted successfully!")
    
    # Organize images into healthy and diseased folders
    print("\nOrganizing images...")
    
    # Create directories
    os.makedirs('test_images/healthy', exist_ok=True)
    os.makedirs('test_images/diseased', exist_ok=True)
    
    # Find the PlantVillage folder
    plantvillage_path = None
    for root, dirs, files in os.walk('plantvillage_temp'):
        if 'PlantVillage' in dirs:
            plantvillage_path = os.path.join(root, 'PlantVillage')
            break
    
    if not plantvillage_path:
        # Try alternative paths
        for root, dirs, files in os.walk('plantvillage_temp'):
            if any('healthy' in d.lower() for d in dirs):
                plantvillage_path = root
                break
    
    if plantvillage_path:
        healthy_count = 0
        diseased_count = 0
        
        # Process each category folder
        for category_folder in os.listdir(plantvillage_path):
            category_path = os.path.join(plantvillage_path, category_folder)
            
            if not os.path.isdir(category_path):
                continue
            
            # Determine if this is a healthy or diseased category
            is_healthy = 'healthy' in category_folder.lower()
            target_dir = 'test_images/healthy' if is_healthy else 'test_images/diseased'
            
            # Copy images from this category
            for img_file in os.listdir(category_path):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    src = os.path.join(category_path, img_file)
                    
                    # Create unique filename
                    prefix = 'healthy' if is_healthy else 'diseased'
                    count = healthy_count if is_healthy else diseased_count
                    ext = os.path.splitext(img_file)[1]
                    dst = os.path.join(target_dir, f'{prefix}_{count:04d}{ext}')
                    
                    shutil.copy2(src, dst)
                    
                    if is_healthy:
                        healthy_count += 1
                    else:
                        diseased_count += 1
                    
                    # Limit to 500 images per category
                    if healthy_count >= 500 and diseased_count >= 500:
                        break
            
            if healthy_count >= 500 and diseased_count >= 500:
                break
        
        print(f"\n✓ Organized {healthy_count} healthy images")
        print(f"✓ Organized {diseased_count} diseased images")
    
    # Cleanup
    print("\nCleaning up temporary files...")
    shutil.rmtree('plantvillage_temp')
    os.remove(zip_file)
    
    print("\n" + "=" * 60)
    print("✓ Download complete!")
    print("=" * 60)
    print(f"\nImages saved in:")
    print(f"  - test_images/healthy/    ({healthy_count} images)")
    print(f"  - test_images/diseased/   ({diseased_count} images)")
    print("\nYou can now upload these images to test the application.")
else:
    print("\n✗ Failed to download dataset")
    print("Please check your Kaggle credentials and try again.")
