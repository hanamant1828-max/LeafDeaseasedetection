import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load the model
model = tf.keras.models.load_model('models/plant_disease_model.keras')

# Test multiple images
test_images = [
    ('xyz/healthy_cucumber_pla_20491dcb.jpg', 'Healthy'),
    ('xyz/healthy_cucumber_pla_381ee0e1.jpg', 'Healthy'),
    ('xyz/healthy_cucumber_pla_7dc41592.jpg', 'Healthy'),
    ('xyz/healthy_green_plant__d277b280.jpg', 'Healthy'),
    ('xyz/diseased_plant_leave_199dde3b.jpg', 'Diseased'),
    ('xyz/diseased_plant_leave_3c47ab27.jpg', 'Diseased'),
    ('xyz/diseased_plant_leave_64417ceb.jpg', 'Diseased'),
    ('xyz/diseased_plant_leave_e958da4b.jpg', 'Diseased'),
]

print("=" * 70)
print("COMPREHENSIVE MODEL TEST")
print("=" * 70)

correct = 0
total = 0

for img_path, true_label in test_images:
    if not os.path.exists(img_path):
        print(f"SKIP: {img_path} not found")
        continue
        
    img = Image.open(img_path)
    img = img.convert('RGB')
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array, verbose=0)
    pred_value = prediction[0][0]
    
    # Current logic: >0.5 = healthy, <=0.5 = diseased
    pred_label = "Healthy" if pred_value > 0.5 else "Diseased"
    is_correct = pred_label == true_label
    correct += is_correct
    total += 1
    
    status = "✓" if is_correct else "✗"
    
    print(f"{status} True: {true_label:8s} | Pred: {pred_label:8s} | Score: {pred_value:.4f} | {os.path.basename(img_path)}")

print("=" * 70)
print(f"Accuracy: {correct}/{total} = {100*correct/total:.1f}%")
print("=" * 70)
