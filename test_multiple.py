import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load the model
model = tf.keras.models.load_model('models/plant_disease_model.keras')

# Test multiple images
test_images = [
    ('xyz/healthy_green_plant__d277b280.jpg', 'Healthy'),
    ('xyz/healthy_plant_leave_66ef3b3a.jpg', 'Healthy'),
    ('xyz/healthy_vibrant_plant_9c3e1c53.jpg', 'Healthy'),
    ('xyz/diseased_plant_leave_e958da4b.jpg', 'Diseased'),
    ('xyz/diseased_plant_wilti_39c08d2f.jpg', 'Diseased'),
    ('xyz/diseased_yellowing_p_7e1d0ee5.jpg', 'Diseased'),
]

print("=" * 70)
print("TESTING MULTIPLE IMAGES")
print("=" * 70)

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
    
    # Current logic: >0.5 = healthy, <0.5 = diseased
    pred_label = "Healthy" if pred_value > 0.5 else "Diseased"
    correct = "✓" if pred_label == true_label else "✗"
    
    print(f"{correct} True: {true_label:8s} | Pred: {pred_label:8s} | Score: {pred_value:.4f} | {os.path.basename(img_path)}")

print("=" * 70)
