#!/usr/bin/env python3
"""
Test the fixed analysis on problematic images
"""
import os
from analysis import DiseaseAnalyzer

# Initialize analyzer with the fix
analyzer = DiseaseAnalyzer()
print(f"Model loaded: {analyzer.model_loaded}\n")

# Test on the images that were incorrectly classified
test_cases = [
    ('uploads/20251031_172140_healthy_pepper_plant_837f539c.jpg', 'healthy', 'Full healthy pepper plant'),
    ('uploads/20251031_172103_healthy_green_plant__f6e461be.jpg', 'healthy', 'Full healthy green plant'),
    ('uploads/20251031_165948_healthy_potato_plant_2e3ff521.jpg', 'healthy', 'Full healthy potato plant'),
    ('uploads/20251031_170143_diseased_plant_leave_e958da4b.jpg', 'diseased', 'Diseased leaf close-up'),
    ('uploads/20251031_170030_diseased_plant_leave_64417ceb.jpg', 'diseased', 'Diseased leaf close-up'),
]

print("="*80)
print("TESTING FIXED ANALYSIS")
print("="*80)

correct = 0
total = 0

for filepath, expected, description in test_cases:
    if not os.path.exists(filepath):
        print(f"\nSkipping {filepath} - not found")
        continue
    
    print(f"\n{'='*80}")
    print(f"Testing: {description}")
    print(f"Expected: {expected}")
    print(f"{'='*80}")
    
    try:
        result = analyzer.analyze_image(filepath)
        predicted = result['disease']
        
        is_correct = predicted == expected
        if is_correct:
            correct += 1
        total += 1
        
        match = "✓ CORRECT" if is_correct else "✗ WRONG"
        
        print(f"{match}")
        print(f"  Predicted: {result['disease_name']}")
        print(f"  Confidence: {result['confidence']:.1f}%")
        print(f"  Severity: {result['severity']}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*80}")
print(f"ACCURACY: {correct}/{total} ({100*correct/total if total > 0 else 0:.1f}%)")
print(f"{'='*80}")
