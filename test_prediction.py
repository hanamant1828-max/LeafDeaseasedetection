import tensorflow as tf
import numpy as np
from PIL import Image

# Load the model
model = tf.keras.models.load_model('models/plant_disease_model.keras')

# Print model summary
print("=" * 50)
print("MODEL SUMMARY:")
print("=" * 50)
model.summary()

# Test with a healthy image
img_path = 'xyz/healthy_green_plant__d277b280.jpg'
img = Image.open(img_path)
img = img.convert('RGB')

# Preprocess
img_resized = img.resize((224, 224))
img_array = np.array(img_resized) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
prediction = model.predict(img_array, verbose=1)

print("\n" + "=" * 50)
print("PREDICTION RESULT:")
print("=" * 50)
print(f"Raw prediction shape: {prediction.shape}")
print(f"Raw prediction value: {prediction}")
print(f"Prediction[0][0]: {prediction[0][0]}")

if prediction[0][0] > 0.5:
    print(f"Classification: HEALTHY (confidence: {prediction[0][0] * 100:.2f}%)")
else:
    print(f"Classification: DISEASED (confidence: {(1 - prediction[0][0]) * 100:.2f}%)")
