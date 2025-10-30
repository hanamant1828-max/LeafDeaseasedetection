
import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create directories
os.makedirs('test_images/healthy', exist_ok=True)
os.makedirs('test_images/diseased', exist_ok=True)

def create_healthy_leaf(filename, size=(400, 300)):
    """Generate a synthetic healthy leaf image"""
    img = Image.new('RGB', size, color=(34, 139, 34))  # Forest green background
    draw = ImageDraw.Draw(img)
    
    # Draw leaf shape (ellipse)
    leaf_color = (50, 205, 50)  # Lime green - healthy color
    margin = 50
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill=leaf_color, outline=(0, 100, 0), width=3)
    
    # Add veins
    center_x = size[0] // 2
    for i in range(5):
        y_pos = margin + (size[1] - 2*margin) * i // 4
        draw.line([(center_x, y_pos), (margin + 20, y_pos)], fill=(0, 128, 0), width=2)
        draw.line([(center_x, y_pos), (size[0] - margin - 20, y_pos)], fill=(0, 128, 0), width=2)
    
    # Add text label
    try:
        draw.text((10, 10), "HEALTHY", fill=(255, 255, 255))
    except:
        pass
    
    img.save(filename)
    print(f"Created: {filename}")

def create_diseased_leaf(filename, size=(400, 300), disease_type="spots"):
    """Generate a synthetic diseased leaf image"""
    img = Image.new('RGB', size, color=(101, 67, 33))  # Brown background
    draw = ImageDraw.Draw(img)
    
    # Draw leaf shape with yellowish color (stressed)
    leaf_color = (154, 205, 50)  # Yellow-green - stressed color
    margin = 50
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill=leaf_color, outline=(139, 69, 19), width=3)
    
    # Add disease patterns
    if disease_type == "spots":
        # Brown spots (fungal disease)
        for _ in range(15):
            x = random.randint(margin + 30, size[0] - margin - 30)
            y = random.randint(margin + 30, size[1] - margin - 30)
            spot_size = random.randint(10, 25)
            draw.ellipse([x-spot_size, y-spot_size, x+spot_size, y+spot_size], 
                        fill=(101, 67, 33), outline=(70, 40, 20), width=2)
    
    elif disease_type == "blight":
        # Blight pattern (brownish areas)
        for _ in range(8):
            x = random.randint(margin + 20, size[0] - margin - 20)
            y = random.randint(margin + 20, size[1] - margin - 20)
            blight_size = random.randint(20, 40)
            draw.ellipse([x-blight_size, y-blight_size, x+blight_size, y+blight_size], 
                        fill=(139, 90, 43), outline=(101, 67, 33), width=1)
    
    elif disease_type == "powdery":
        # White powdery mildew
        for _ in range(25):
            x = random.randint(margin + 30, size[0] - margin - 30)
            y = random.randint(margin + 30, size[1] - margin - 30)
            powder_size = random.randint(5, 15)
            draw.ellipse([x-powder_size, y-powder_size, x+powder_size, y+powder_size], 
                        fill=(245, 245, 245), outline=(220, 220, 220), width=1)
    
    # Add text label
    try:
        draw.text((10, 10), "DISEASED", fill=(255, 255, 255))
    except:
        pass
    
    img.save(filename)
    print(f"Created: {filename}")

print("Generating synthetic test images...")
print("=" * 50)

# Generate healthy leaf images
print("\nGenerating HEALTHY plant images:")
for i in range(1, 4):
    create_healthy_leaf(f'test_images/healthy/healthy_leaf_{i}.png')

# Generate diseased leaf images
print("\nGenerating DISEASED plant images:")
create_diseased_leaf('test_images/diseased/fungal_spots_1.png', disease_type="spots")
create_diseased_leaf('test_images/diseased/fungal_spots_2.png', disease_type="spots")
create_diseased_leaf('test_images/diseased/early_blight_1.png', disease_type="blight")
create_diseased_leaf('test_images/diseased/late_blight_1.png', disease_type="blight")
create_diseased_leaf('test_images/diseased/powdery_mildew_1.png', disease_type="powdery")

print("\n" + "=" * 50)
print("Image generation complete!")
print(f"\nTest images created in:")
print(f"  - test_images/healthy/    (3 images)")
print(f"  - test_images/diseased/   (5 images)")
print("\nYou can now use these images to test the application.")
print("Upload them through the web interface to test disease detection.")
