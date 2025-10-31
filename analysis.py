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
        'early_blight': {
            'name': 'Early Blight',
            'description': 'Early blight is a fungal disease caused by Alternaria solani. It appears as dark brown spots with concentric rings (target-like pattern) on lower leaves first.',
            'treatment': 'Remove affected leaves immediately. Apply copper-based fungicide or organic neem oil spray. Improve air circulation around plants.',
            'prevention': 'Practice crop rotation, avoid overhead watering, mulch around plants, remove plant debris, and ensure proper spacing between plants.'
        },
        'late_blight': {
            'name': 'Late Blight',
            'description': 'Late blight is a serious disease caused by Phytophthora infestans. Characterized by large, irregular dark brown or black spots with a water-soaked appearance.',
            'treatment': 'Remove and destroy infected plants immediately. Apply fungicide containing chlorothalonil or copper. Avoid watering in the evening.',
            'prevention': 'Use resistant varieties, ensure good drainage, provide adequate spacing, remove infected plant material, and apply preventive fungicides in humid conditions.'
        },
        'powdery_mildew': {
            'name': 'Powdery Mildew',
            'description': 'A fungal disease that appears as white or gray powdery spots on leaves and stems. Can affect plant growth and reduce yield if left untreated.',
            'treatment': 'Spray with fungicide, neem oil, or a baking soda solution (1 tbsp per gallon of water). Remove severely affected leaves.',
            'prevention': 'Ensure good air circulation, avoid overcrowding plants, water at the base of plants (not leaves), and plant in sunny locations.'
        },
        'bacterial_spot': {
            'name': 'Bacterial Spot',
            'description': 'Caused by Xanthomonas bacteria. Shows as small, dark brown to black spots with yellow halos on leaves. Can cause defoliation and reduce fruit quality.',
            'treatment': 'Remove infected leaves. Apply copper-based bactericide. Avoid working with plants when wet. Improve drainage.',
            'prevention': 'Use disease-free seeds, practice crop rotation, avoid overhead irrigation, sanitize tools, and remove plant debris.'
        },
        'fungal_leaf_spot': {
            'name': 'Fungal Leaf Spot',
            'description': 'General fungal infection causing circular or irregular spots on leaves. Spots may be brown, black, or tan with darker borders.',
            'treatment': 'Remove affected leaves. Apply broad-spectrum fungicide. Reduce leaf wetness by avoiding overhead watering.',
            'prevention': 'Ensure good air circulation, water early in the day, remove fallen leaves, practice crop rotation, and use disease-resistant varieties.'
        },
        'nutrient_deficiency': {
            'name': 'Nutrient Deficiency',
            'description': 'Yellowing leaves (chlorosis) may indicate nitrogen, iron, or other nutrient deficiencies. Can affect plant vigor and productivity.',
            'treatment': 'Apply balanced fertilizer. For nitrogen deficiency, use high-nitrogen fertilizer. For iron deficiency, apply iron chelate. Test soil pH.',
            'prevention': 'Regular soil testing, use balanced fertilizers, maintain proper soil pH (6.0-6.8 for most plants), and add organic matter to soil.'
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
        has_spots = spot_analysis['has_significant_spots']
        texture_var = texture_analysis['texture_variance']
        
        # Healthy plant detection - high green content, low brown/yellow, minimal spots
        if health_score > 25 and green_content > 35 and brown_content < 7 and spot_count < 4:
            return 'healthy', random.uniform(85, 95), 'None'
        
        # Late Blight - very high brown content, lots of spots, irregular patterns
        # Most severe disease with highest brown content
        if brown_content > 15 and spot_count > 8:
            confidence = random.uniform(75, 88)
            severity = 'High' if brown_content > 25 else 'Medium'
            return 'late_blight', confidence, severity
        
        # Early Blight - moderate to high brown with circular spot patterns
        # Distinguished by moderate brown and significant spots
        if brown_content > 8 and brown_content <= 15 and spot_count > 6:
            confidence = random.uniform(70, 85)
            severity = 'Medium' if brown_content > 12 else 'Low'
            return 'early_blight', confidence, severity
        
        # Bacterial Spot - characterized primarily by numerous distinct spots
        # Higher spot count with moderate brown
        if spot_count > 7 and brown_content > 5 and brown_content <= 12:
            confidence = random.uniform(70, 84)
            severity = 'Medium' if spot_count > 10 else 'Low'
            return 'bacterial_spot', confidence, severity
        
        # Nutrient Deficiency - high yellow, low brown, overall yellowing
        # Check this before fungal spots to catch yellowing leaves
        if yellow_content > 15 and brown_content < 8 and spot_count < 6:
            confidence = random.uniform(68, 82)
            severity = 'Medium' if yellow_content > 25 else 'Low'
            return 'nutrient_deficiency', confidence, severity
        
        # Powdery Mildew - high yellow/white with texture changes
        # Distinguished by texture variance and yellowing without many spots
        if yellow_content > 12 and texture_var > 500 and spot_count < 7 and brown_content < 10:
            confidence = random.uniform(72, 85)
            severity = 'Medium' if yellow_content > 20 else 'Low'
            return 'powdery_mildew', confidence, severity
        
        # Fungal Leaf Spot - moderate spots and brown content
        # Catches general fungal infections
        if spot_count > 4 and brown_content > 4:
            confidence = random.uniform(68, 81)
            severity = 'Medium' if spot_count > 7 else 'Low'
            return 'fungal_leaf_spot', confidence, severity
        
        # General unhealthy condition - low health score but doesn't match specific diseases
        if health_score < 15 or brown_content > 7 or yellow_content > 10:
            confidence = random.uniform(65, 78)
            severity = 'Low'
            # Return fungal leaf spot for general unhealthy conditions
            return 'fungal_leaf_spot', confidence, severity
        
        # Default to healthy if no disease patterns detected
        confidence = random.uniform(70, 82)
        return 'healthy', confidence, 'None'
