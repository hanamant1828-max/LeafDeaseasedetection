#!/usr/bin/env python3
"""
Test the complete upload and analysis workflow
"""
import os
import shutil
from analysis import DiseaseAnalyzer

# Initialize analyzer (same as in app.py)
print("Initializing DiseaseAnalyzer...")
analyzer = DiseaseAnalyzer()
print(f"Model loaded: {analyzer.model_loaded}")
print(f"Model object: {analyzer.model is not None}\n")

# Test images
test_cases = [
    ('test_images/healthy/healthy_leaf_1.png', 'healthy'),
    ('test_images/healthy/healthy_leaf_2.png', 'healthy'),
    ('test_images/diseased/early_blight_1.png', 'diseased'),
    ('test_images/diseased/fungal_spots_1.png', 'diseased'),
]

print("="*80)
print("TESTING COMPLETE UPLOAD WORKFLOW")
print("="*80)

correct = 0
total = 0

for img_path, expected in test_cases:
    if not os.path.exists(img_path):
        print(f"\nSkipping {img_path} - not found")
        continue
    
    print(f"\n{'='*80}")
    print(f"Testing: {os.path.basename(img_path)}")
    print(f"Expected: {expected}")
    print(f"{'='*80}")
    
    # Simulate upload by copying to uploads directory
    upload_path = os.path.join('uploads', 'test_' + os.path.basename(img_path))
    shutil.copy(img_path, upload_path)
    
    try:
        # Analyze image (same as app.py does)
        result = analyzer.analyze_image(upload_path)
        
        predicted = result['disease']
        is_correct = predicted == expected
        
        if is_correct:
            correct += 1
        total += 1
        
        match = "✓ CORRECT" if is_correct else "✗ INCORRECT"
        
        print(f"\n{match}")
        print(f"  Disease: {result['disease_name']}")
        print(f"  Confidence: {result['confidence']:.1f}%")
        print(f"  Severity: {result['severity']}")
        print(f"  ML Powered: {result['analysis_details']['ml_powered']}")
        print(f"  Green content: {result['analysis_details']['green_content']:.1f}%")
        print(f"  Brown content: {result['analysis_details']['brown_content']:.1f}%")
        print(f"  Yellow content: {result['analysis_details']['yellow_content']:.1f}%")
        print(f"  Spots detected: {result['analysis_details']['spots_detected']:.1f}%")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        if os.path.exists(upload_path):
            os.remove(upload_path)

print(f"\n{'='*80}")
print(f"FINAL ACCURACY: {correct}/{total} ({100*correct/total if total > 0 else 0:.1f}%)")
print(f"{'='*80}")
