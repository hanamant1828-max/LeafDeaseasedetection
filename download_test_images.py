
import os
import urllib.request

# Create test_images directory
os.makedirs('test_images/healthy', exist_ok=True)
os.makedirs('test_images/diseased', exist_ok=True)

# Sample images from PlantVillage dataset (public domain)
test_images = {
    'healthy': [
        ('https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Tomato___healthy/0a88f628-bd38-4cdf-9911-ec54907d9769___RS_HL%207537.JPG', 'tomato_healthy_1.jpg'),
        ('https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Potato___healthy/0a5cff51-7843-4aea-a0ca-70ce7bbe3cde___RS_HL%208527.JPG', 'potato_healthy_1.jpg'),
        ('https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Pepper%2C_bell___healthy/0a64165d-7bcb-4d95-a88c-76aacf69f5b4___JR_HL%208588.JPG', 'pepper_healthy_1.jpg'),
    ],
    'diseased': [
        ('https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Tomato___Early_blight/0a3e3095-6eab-4b0e-afa2-d9e9618e4c1e___RS_Early.B%206368.JPG', 'tomato_early_blight_1.jpg'),
        ('https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Tomato___Late_blight/0a217eae-80be-4903-8e5e-e25c9fedea1d___RS_Late.B%204946.JPG', 'tomato_late_blight_1.jpg'),
        ('https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Potato___Early_blight/0a0b0c63-28c6-43ea-8692-e5b0e1e40197___RS_Early.B%207506.JPG', 'potato_early_blight_1.jpg'),
        ('https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Pepper%2C_bell___Bacterial_spot/0a2e96c7-7e50-465e-8b12-77fd7f09c2e8___JR_B.Spot%203086.JPG', 'pepper_bacterial_spot_1.jpg'),
    ]
}

print("Downloading test images...")
print("=" * 50)

for category, images in test_images.items():
    print(f"\n{category.upper()} PLANTS:")
    for url, filename in images:
        try:
            filepath = os.path.join('test_images', category, filename)
            print(f"  Downloading {filename}...", end=' ')
            urllib.request.urlretrieve(url, filepath)
            print("✓ Done")
        except Exception as e:
            print(f"✗ Failed: {e}")

print("\n" + "=" * 50)
print("Download complete!")
print(f"\nTest images saved in:")
print(f"  - test_images/healthy/    ({len(test_images['healthy'])} images)")
print(f"  - test_images/diseased/   ({len(test_images['diseased'])} images)")
print("\nYou can now upload these images to test the application.")
