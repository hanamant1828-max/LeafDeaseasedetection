import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import random
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock disease database
DISEASES = [
    {
        "name": "Early Blight",
        "confidence": 0.85,
        "severity": "Moderate",
        "description": "A common fungal disease affecting tomatoes and potatoes. Causes dark spots with concentric rings on leaves.",
        "treatment": "Apply fungicide spray and ensure proper plant spacing for air circulation.",
        "prevention": "Rotate crops, avoid overhead watering, and remove infected plant debris."
    },
    {
        "name": "Late Blight",
        "confidence": 0.92,
        "severity": "Severe",
        "description": "A serious disease that can quickly destroy tomato and potato crops in humid conditions.",
        "treatment": "Immediate fungicide application and removal of affected plant parts.",
        "prevention": "Use resistant varieties and avoid watering leaves directly."
    },
    {
        "name": "Powdery Mildew",
        "confidence": 0.78,
        "severity": "Mild",
        "description": "White powdery coating on leaves that can reduce plant vigor and yield.",
        "treatment": "Apply sulfur-based fungicide or baking soda solution.",
        "prevention": "Ensure good air circulation and avoid crowding plants."
    },
    {
        "name": "Bacterial Spot",
        "confidence": 0.88,
        "severity": "Moderate",
        "description": "Small dark spots on leaves that may have yellow halos, affecting peppers and tomatoes.",
        "treatment": "Use copper-based bactericides and remove infected plant material.",
        "prevention": "Use pathogen-free seeds and avoid overhead irrigation."
    },
    {
        "name": "Healthy",
        "confidence": 0.95,
        "severity": "None",
        "description": "The plant appears healthy with no visible signs of disease.",
        "treatment": "No treatment needed. Continue regular care and monitoring.",
        "prevention": "Maintain good growing conditions and regular plant health checks."
    }
]

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_path):
    """Validate that the uploaded file is a valid image."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception as e:
        logging.error(f"Image validation failed: {e}")
        return False

def mock_disease_prediction(image_path):
    """Mock ML prediction function that returns random disease prediction."""
    # Simulate processing time
    import time
    time.sleep(1)
    
    # Return random disease prediction
    disease = random.choice(DISEASES)
    
    # Add some randomness to confidence
    confidence_variation = random.uniform(-0.1, 0.1)
    disease["confidence"] = max(0.1, min(0.99, disease["confidence"] + confidence_variation))
    
    return disease

@app.route('/')
def index():
    """Main page with upload form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and disease prediction."""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF, BMP, WEBP)', 'error')
        return redirect(url_for('index'))
    
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)
        
        # Validate the image
        if not validate_image(file_path):
            os.remove(file_path)  # Clean up invalid file
            flash('Invalid image file. Please upload a valid image.', 'error')
            return redirect(url_for('index'))
        
        # Mock disease prediction
        prediction = mock_disease_prediction(file_path)
        
        # Clean up uploaded file (in production, you might want to keep it)
        os.remove(file_path)
        
        return render_template('index.html', prediction=prediction, success=True)
        
    except Exception as e:
        logging.error(f"Error processing upload: {e}")
        flash('An error occurred while processing your image. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for disease prediction (for future AJAX integration)."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        if not validate_image(file_path):
            os.remove(file_path)
            return jsonify({'error': 'Invalid image file'}), 400
        
        prediction = mock_disease_prediction(file_path)
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        logging.error(f"API prediction error: {e}")
        return jsonify({'error': 'Processing failed'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash('File too large. Please upload an image smaller than 16MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
