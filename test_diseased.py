import tensorflow as tf
import numpy as np
from PIL import Image

# Load the model
model = tf.keras.models.load_model('models/plant_disease_model.keras')

# Test with a diseased image
img_path = 'xyz/diseased_plant_leave_e958da4b.jpg'
img = Image.open(img_path)
img = img.convert('RGB')

# Preprocess
img_resized = img.resize((224, 224))
img_array = np.array(img_resized) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
prediction = model.predict(img_array, verbose=0)

print("=" * 50)
print("TESTING DISEASED IMAGE")
print("=" * 50)
print(f"Image: {img_path}")
print(f"Prediction value: {prediction[0][0]}")

if prediction[0][0] > 0.5:
    print(f"Current logic says: HEALTHY (confidence: {prediction[0][0] * 100:.2f}%)")
else:
    print(f"Current logic says: DISEASED (confidence: {(1 - prediction[0][0]) * 100:.2f}%)")
