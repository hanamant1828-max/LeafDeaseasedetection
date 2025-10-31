#!/usr/bin/env python3
"""
Debug recent uploads to see what predictions were made
"""
import os
from analysis import DiseaseAnalyzer

# Initialize analyzer
analyzer = DiseaseAnalyzer()
print(f"Model loaded: {analyzer.model_loaded}\n")

# Get recent uploads
uploads_dir = 'uploads'
recent_files = sorted(
    [(f, os.path.getmtime(os.path.join(uploads_dir, f))) 
     for f in os.listdir(uploads_dir) if f.endswith(('.jpg', '.png', '.jpeg'))],
    key=lambda x: x[1],
    reverse=True
)[:10]

print("="*80)
print("ANALYZING RECENT UPLOADS")
print("="*80)

for filename, _ in recent_files:
    filepath = os.path.join(uploads_dir, filename)
    
    # Extract expected label from filename if possible
    expected = None
    if 'healthy' in filename.lower():
        expected = 'healthy'
    elif 'diseased' in filename.lower() or 'disease' in filename.lower() or 'blight' in filename.lower() or 'mildew' in filename.lower():
        expected = 'diseased'
    
    print(f"\n{'='*80}")
    print(f"File: {filename}")
    if expected:
        print(f"Expected (from filename): {expected}")
    print(f"{'='*80}")
    
    try:
        result = analyzer.analyze_image(filepath)
        predicted = result['disease']
        
        match = ""
        if expected:
            match = " ✓ CORRECT" if predicted == expected else " ✗ WRONG"
        
        print(f"Predicted: {result['disease_name']}{match}")
        print(f"Confidence: {result['confidence']:.1f}%")
        print(f"Severity: {result['severity']}")
        print(f"ML Powered: {result['analysis_details']['ml_powered']}")
        
    except Exception as e:
        print(f"ERROR: {e}")

print(f"\n{'='*80}")
