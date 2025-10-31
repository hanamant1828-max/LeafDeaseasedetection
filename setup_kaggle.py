
import os
import json
from pathlib import Path

print("=" * 60)
print("Kaggle API Setup Helper")
print("=" * 60)

# Get credentials from user
print("\nTo download datasets from Kaggle, you need API credentials.")
print("\nTo get your Kaggle API credentials:")
print("1. Go to https://www.kaggle.com/account")
print("2. Scroll to 'API' section")
print("3. Click 'Create New Token'")
print("4. This will download 'kaggle.json' file")
print("\n" + "=" * 60)

username = input("\nEnter your Kaggle username: ").strip()
key = input("Enter your Kaggle API key: ").strip()

if username and key:
    # Create .kaggle directory
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    
    # Create kaggle.json
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    credentials = {
        "username": username,
        "key": key
    }
    
    with open(kaggle_json, 'w') as f:
        json.dump(credentials, f)
    
    # Set proper permissions
    os.chmod(kaggle_json, 0o600)
    
    print("\n✓ Kaggle credentials saved successfully!")
    print(f"✓ Credentials saved to: {kaggle_json}")
    print("\nYou can now run: python download_kaggle_dataset.py")
else:
    print("\n✗ Invalid credentials. Please try again.")
