import os
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

# Dataset to download
DATASET = 'vipoooool/new-plant-diseases-dataset'
DOWNLOAD_PATH = './kaggle_dataset'

print(f"Downloading dataset: {DATASET}")
print("This may take a few minutes...")

# Download the dataset
api.dataset_download_files(DATASET, path=DOWNLOAD_PATH, unzip=True)

print(f"\nDataset downloaded successfully to: {DOWNLOAD_PATH}")

# List the downloaded files
if os.path.exists(DOWNLOAD_PATH):
    print("\nDownloaded files:")
    for root, dirs, files in os.walk(DOWNLOAD_PATH):
        level = root.replace(DOWNLOAD_PATH, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        if level < 2:  # Only show first 2 levels to avoid too much output
            for file in files[:5]:  # Show first 5 files
                print(f'{subindent}{file}')
            if len(files) > 5:
                print(f'{subindent}... and {len(files) - 5} more files')
