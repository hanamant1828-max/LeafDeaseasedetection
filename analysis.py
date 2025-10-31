import os
import numpy as np
from PIL import Image, ImageStat
import logging

logger = logging.getLogger(__name__)

class DiseaseAnalyzer:
    
    DISEASE_DATABASE = {
        'healthy': {
            'name': 'Healthy Plant',
            'description': 'The plant appears to be in good health with no visible signs of disease. The leaf shows vibrant green coloration and no abnormal spots or discoloration.',
            'treatment': 'No treatment needed. Continue regular care routine.',
            'prevention': 'Maintain proper watering schedule, ensure adequate sunlight, use balanced fertilizer, and monitor regularly for early signs of disease.'
        },
        'diseased': {
            'name': 'Diseased Plant',
            'description': 'The plant shows signs of disease, including discoloration, spots, or other abnormalities. Common causes include fungal infections, bacterial diseases, or nutrient deficiencies.',
            'treatment': 'Remove affected leaves immediately. Apply appropriate fungicide or bactericide. Improve air circulation and reduce leaf wetness. Consult a local agricultural expert for specific treatment recommendations.',
            'prevention': 'Practice crop rotation, avoid overhead watering, ensure proper plant spacing, remove plant debris, use disease-resistant varieties, and maintain proper soil nutrition and pH levels.'
        }
    }
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        try:
            import tensorflow as tf
            model_path = 'models/plant_disease_model.keras'
            
            if os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
                self.model_loaded = True
                logger.info(f"ML model loaded successfully from {model_path}")
            else:
                logger.warning(f"Model not found at {model_path}, using rule-based analysis")
                self.model_loaded = False
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            self.model_loaded = False
    
    def analyze_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.convert('RGB')
            
            if self.model_loaded and self.model is not None:
                disease, confidence, severity = self._ml_predict(img)
            else:
                color_analysis = self._analyze_colors(img)
                spot_analysis = self._detect_spots(img)
                texture_analysis = self._analyze_texture(img)
                disease, confidence, severity = self._determine_disease(
                    color_analysis, spot_analysis, texture_analysis
                )
            
            color_analysis = self._analyze_colors(img)
            spot_analysis = self._detect_spots(img)
            
            disease_info = self.DISEASE_DATABASE.get(disease, self.DISEASE_DATABASE['healthy'])
            
            return {
                'disease': disease,
                'disease_name': disease_info['name'],
                'confidence': confidence,
                'severity': severity,
                'description': disease_info['description'],
                'treatment': disease_info['treatment'],
                'prevention': disease_info['prevention'],
                'analysis_details': {
                    'green_content': color_analysis['green_percentage'],
                    'brown_content': color_analysis['brown_percentage'],
                    'yellow_content': color_analysis['yellow_percentage'],
                    'spots_detected': spot_analysis['spot_count'],
                    'overall_health': color_analysis['health_score'],
                    'ml_powered': self.model_loaded
                }
            }
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            raise Exception(f"Image analysis failed: {str(e)}")
    
    def _ml_predict(self, img):
        try:
            import tensorflow as tf
            
            img_resized = img.resize((224, 224))
            img_array = np.array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            prediction = self.model.predict(img_array, verbose=0)[0][0]
            
            # Model trained with flow_from_directory: diseased=0, healthy=1
            # prediction close to 1 = healthy, close to 0 = diseased
            if prediction > 0.5:
                disease = 'healthy'
                confidence = float(prediction * 100)
                severity = 'None'
            else:
                disease = 'diseased'
                confidence = float((1 - prediction) * 100)
                
                if prediction < 0.2:
                    severity = 'High'
                elif prediction < 0.35:
                    severity = 'Medium'
                else:
                    severity = 'Low'
            
            return disease, confidence, severity
            
        except Exception as e:
            logger.error(f"ML prediction failed: {e}, falling back to rule-based")
            color_analysis = self._analyze_colors(img)
            spot_analysis = self._detect_spots(img)
            texture_analysis = self._analyze_texture(img)
            return self._determine_disease(color_analysis, spot_analysis, texture_analysis)
    
    def _analyze_colors(self, img):
        pixels = np.array(img)
        height, width, _ = pixels.shape
        total_pixels = height * width
        
        r = pixels[:, :, 0].flatten()
        g = pixels[:, :, 1].flatten()
        b = pixels[:, :, 2].flatten()
        
        green_mask = (g > r) & (g > b) & (g > 50)
        green_pixels = np.sum(green_mask)
        green_percentage = (green_pixels / total_pixels) * 100
        
        brown_mask = ((r > 80) & (r < 220) & (g > 40) & (g < 180) & (b < 120) & (r > b))
        brown_pixels = np.sum(brown_mask)
        brown_percentage = (brown_pixels / total_pixels) * 100
        
        yellow_mask = ((r > 120) & (g > 120) & (b < 120) & (r > b) & (g > b))
        yellow_pixels = np.sum(yellow_mask)
        yellow_percentage = (yellow_pixels / total_pixels) * 100
        
        health_score = green_percentage - (brown_percentage + yellow_percentage * 0.7)
        
        return {
            'green_percentage': round(green_percentage, 2),
            'brown_percentage': round(brown_percentage, 2),
            'yellow_percentage': round(yellow_percentage, 2),
            'health_score': round(health_score, 2)
        }
    
    def _detect_spots(self, img):
        img_gray = img.convert('L')
        pixels = np.array(img_gray)
        
        threshold = np.mean(pixels) - (np.std(pixels) * 0.8)
        dark_spots = pixels < threshold
        
        spot_count = np.sum(dark_spots) / pixels.size * 100
        
        return {
            'spot_count': round(spot_count, 2),
            'has_significant_spots': spot_count > 8
        }
    
    def _analyze_texture(self, img):
        stat = ImageStat.Stat(img.convert('L'))
        variance = stat.var[0]
        
        return {
            'texture_variance': variance,
            'is_uniform': variance < 500
        }
    
    def _determine_disease(self, color_analysis, spot_analysis, texture_analysis):
        health_score = color_analysis['health_score']
        brown_content = color_analysis['brown_percentage']
        yellow_content = color_analysis['yellow_percentage']
        green_content = color_analysis['green_percentage']
        spot_count = spot_analysis['spot_count']
        
        discoloration_score = brown_content + (yellow_content * 0.7)
        
        is_healthy = (
            green_content > 15 and
            discoloration_score < 15 and
            spot_count < 8 and
            health_score > 0
        )
        
        if is_healthy:
            confidence_base = min(95, 75 + (green_content / 2))
            confidence_penalty = (brown_content + yellow_content + spot_count) * 0.5
            confidence = max(70, confidence_base - confidence_penalty)
            return 'healthy', float(confidence), 'None'
        else:
            confidence_base = 70
            if discoloration_score > 20:
                confidence_base += 10
            if spot_count > 10:
                confidence_base += 5
            if green_content < 10:
                confidence_base += 10
            
            confidence = min(95, confidence_base)
            
            severity_score = (brown_content * 1.5) + yellow_content + (spot_count * 0.8)
            
            if severity_score > 30 or green_content < 8:
                severity = 'High'
            elif severity_score > 15 or brown_content > 10:
                severity = 'Medium'
            else:
                severity = 'Low'
            
            return 'diseased', float(confidence), severity
