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
        
        # Improved green detection - more inclusive
        green_mask = (g > r) & (g > b) & (g > 50)
        green_pixels = np.sum(green_mask)
        green_percentage = (green_pixels / total_pixels) * 100
        
        # Improved brown detection - catches disease discoloration better
        brown_mask = ((r > 80) & (r < 220) & (g > 40) & (g < 180) & (b < 120) & (r > b))
        brown_pixels = np.sum(brown_mask)
        brown_percentage = (brown_pixels / total_pixels) * 100
        
        # Improved yellow detection - catches chlorosis
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
        
        # More sensitive spot detection
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
        
        # Calculate disease indicators
        discoloration_score = brown_content + (yellow_content * 0.7)
        
        # More lenient and accurate classification
        # Healthy criteria: predominantly green with minimal disease signs
        is_healthy = (
            green_content > 15 and  # More lenient green threshold
            discoloration_score < 15 and  # Combined discoloration threshold
            spot_count < 8 and  # More tolerant of minor spots
            health_score > 0  # Overall positive health score
        )
        
        if is_healthy:
            # Calculate confidence based on how strongly healthy it appears
            confidence_base = min(95, 75 + (green_content / 2))
            confidence_penalty = (brown_content + yellow_content + spot_count) * 0.5
            confidence = max(70, confidence_base - confidence_penalty)
            return 'healthy', confidence, 'None'
        
        # Diseased classification
        else:
            # Calculate confidence based on disease indicators
            confidence_base = 70
            if discoloration_score > 20:
                confidence_base += 10
            if spot_count > 10:
                confidence_base += 5
            if green_content < 10:
                confidence_base += 10
            
            confidence = min(95, confidence_base)
            
            # Determine severity based on multiple factors
            severity_score = (brown_content * 1.5) + yellow_content + (spot_count * 0.8)
            
            if severity_score > 30 or green_content < 8:
                severity = 'High'
            elif severity_score > 15 or brown_content > 10:
                severity = 'Medium'
            else:
                severity = 'Low'
            
            return 'diseased', confidence, severity
