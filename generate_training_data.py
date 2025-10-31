#!/usr/bin/env python3
"""
Generate training dataset by augmenting existing test images.
Creates 500 healthy and 500 diseased images using rotation, flip, brightness, etc.
"""
import os
import shutil
import random
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path

# Configuration
SOURCE_HEALTHY_DIR = './test_images/healthy'
SOURCE_DISEASED_DIR = './test_images/diseased'
TARGET_HEALTHY_DIR = './training_data/healthy'
TARGET_DISEASED_DIR = './training_data/diseased'
NUM_HEALTHY = 500
NUM_DISEASED = 500

def augment_image(img):
    """Apply random augmentation to an image"""
    # Random rotation
    if random.random() > 0.5:
        angle = random.randint(-30, 30)
        img = img.rotate(angle, fillcolor='white')
    
    # Random flip
    if random.random() > 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if random.random() > 0.5:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    
    # Random brightness
    if random.random() > 0.5:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.7, 1.3))
    
    # Random contrast
    if random.random() > 0.5:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(random.uniform(0.8, 1.2))
    
    # Random blur
    if random.random() > 0.3:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0, 1.5)))
    
    # Random crop and resize
    if random.random() > 0.3:
        width, height = img.size
        crop_factor = random.uniform(0.8, 0.95)
        new_width = int(width * crop_factor)
        new_height = int(height * crop_factor)
        left = random.randint(0, width - new_width)
        top = random.randint(0, height - new_height)
        img = img.crop((left, top, left + new_width, top + new_height))
        img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    return img

def generate_images(source_dir, target_dir, num_images, category_name):
    """Generate augmented images from source directory"""
    os.makedirs(target_dir, exist_ok=True)
    
    # Get all source images
    source_images = [f for f in os.listdir(source_dir) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not source_images:
        print(f"  ❌ No images found in {source_dir}")
        return 0
    
    print(f"  Found {len(source_images)} source images")
    print(f"  Generating {num_images} augmented images...")
    
    generated = 0
    for i in range(num_images):
        # Select random source image
        source_file = random.choice(source_images)
        source_path = os.path.join(source_dir, source_file)
        
        try:
            # Load and augment
            img = Image.open(source_path)
            img = img.convert('RGB')  # Ensure RGB format
            
            # Apply augmentation
            augmented = augment_image(img)
            
            # Save
            target_file = f'{category_name}_{i+1:04d}.jpg'
            target_path = os.path.join(target_dir, target_file)
            augmented.save(target_path, 'JPEG', quality=95)
            
            generated += 1
            
            if (i + 1) % 100 == 0:
                print(f"    ✓ Generated {i+1}/{num_images}")
        
        except Exception as e:
            print(f"    ⚠ Error processing {source_file}: {e}")
    
    return generated

def main():
    print("="*60)
    print("PLANT DISEASE TRAINING DATA GENERATOR")
    print("="*60)
    print("Using image augmentation to create training dataset")
    print(f"Source: {SOURCE_HEALTHY_DIR}, {SOURCE_DISEASED_DIR}")
    print(f"Target: {TARGET_HEALTHY_DIR}, {TARGET_DISEASED_DIR}")
    print("="*60)
    
    # Check if source directories exist
    if not os.path.exists(SOURCE_HEALTHY_DIR):
        print(f"❌ Error: {SOURCE_HEALTHY_DIR} does not exist")
        return
    if not os.path.exists(SOURCE_DISEASED_DIR):
        print(f"❌ Error: {SOURCE_DISEASED_DIR} does not exist")
        return
    
    # Generate healthy images
    print("\nStep 1: Generating HEALTHY images")
    healthy_count = generate_images(SOURCE_HEALTHY_DIR, TARGET_HEALTHY_DIR, NUM_HEALTHY, 'healthy')
    
    # Generate diseased images
    print("\nStep 2: Generating DISEASED images")
    diseased_count = generate_images(SOURCE_DISEASED_DIR, TARGET_DISEASED_DIR, NUM_DISEASED, 'diseased')
    
    # Summary
    print("\n" + "="*60)
    print("✓ GENERATION COMPLETE!")
    print("="*60)
    print(f"✓ {healthy_count} healthy images → {TARGET_HEALTHY_DIR}")
    print(f"✓ {diseased_count} diseased images → {TARGET_DISEASED_DIR}")
    print("="*60)
    print("\nAugmentation techniques applied:")
    print("  - Random rotation (-30° to +30°)")
    print("  - Random horizontal/vertical flips")
    print("  - Random brightness adjustment")
    print("  - Random contrast adjustment")
    print("  - Random Gaussian blur")
    print("  - Random crop and resize")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
