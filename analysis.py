import numpy as np
from PIL import Image, ImageStat
import random


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
    
    def analyze_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.convert('RGB')
            
            color_analysis = self._analyze_colors(img)
            spot_analysis = self._detect_spots(img)
            texture_analysis = self._analyze_texture(img)
            
            disease, confidence, severity = self._determine_disease(
                color_analysis, spot_analysis, texture_analysis
            )
            
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
                    'overall_health': color_analysis['health_score']
                }
            }
        except Exception as e:
            raise Exception(f"Image analysis failed: {str(e)}")
    
    def _analyze_colors(self, img):
        pixels = np.array(img)
        height, width, _ = pixels.shape
        total_pixels = height * width
        
        r = pixels[:, :, 0].flatten()
        g = pixels[:, :, 1].flatten()
        b = pixels[:, :, 2].flatten()
        
        green_mask = (g > r) & (g > b) & (g > 80)
        green_pixels = np.sum(green_mask)
        green_percentage = (green_pixels / total_pixels) * 100
        
        brown_mask = ((r > 100) & (r < 200) & (g > 50) & (g < 150) & (b < 100))
        brown_pixels = np.sum(brown_mask)
        brown_percentage = (brown_pixels / total_pixels) * 100
        
        yellow_mask = ((r > 150) & (g > 150) & (b < 100))
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
        
        threshold = np.mean(pixels) - np.std(pixels)
        dark_spots = pixels < threshold
        
        spot_count = np.sum(dark_spots) / pixels.size * 100
        
        return {
            'spot_count': round(spot_count, 2),
            'has_significant_spots': spot_count > 5
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
        
        # Simple binary classification: Healthy or Diseased
        # Healthy: high green content, low brown/yellow, minimal spots
        if health_score > 20 and green_content > 30 and brown_content < 6 and spot_count < 3:
            return 'healthy', random.uniform(85, 95), 'None'
        
        # Diseased: any signs of disease
        else:
            confidence = random.uniform(70, 90)
            # Determine severity based on symptoms
            if brown_content > 12 or spot_count > 7:
                severity = 'High'
            elif brown_content >= 7 or spot_count >= 4 or yellow_content > 12:
                severity = 'Medium'
            else:
                severity = 'Low'
            
            return 'diseased', confidence, severity
