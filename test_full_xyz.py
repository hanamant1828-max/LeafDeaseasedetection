#!/usr/bin/env python3
"""
Test on ALL xyz folder images (not just 15)
"""
import os
from analysis import DiseaseAnalyzer

analyzer = DiseaseAnalyzer()
print(f"Model loaded: {analyzer.model_loaded}\n")

xyz_dir = 'xyz'
all_files = sorted([f for f in os.listdir(xyz_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])

# Categorize ALL files
healthy_files = [f for f in all_files if f.startswith('healthy_')]
diseased_files = [f for f in all_files if not f.startswith('healthy_')]

print("="*80)
print(f"COMPLETE XYZ FOLDER TEST - ALL {len(all_files)} IMAGES")
print("="*80)

healthy_correct = 0
healthy_wrong = 0
diseased_correct = 0
diseased_wrong = 0

# Test ALL healthy images
for filename in healthy_files:
    filepath = os.path.join(xyz_dir, filename)
    try:
        result = analyzer.analyze_image(filepath)
        if result['disease'] == 'healthy':
            healthy_correct += 1
        else:
            healthy_wrong += 1
    except Exception as e:
        print(f"ERROR on {filename}: {e}")
        healthy_wrong += 1

# Test ALL diseased images  
for filename in diseased_files:
    filepath = os.path.join(xyz_dir, filename)
    try:
        result = analyzer.analyze_image(filepath)
        if result['disease'] == 'diseased':
            diseased_correct += 1
        else:
            diseased_wrong += 1
    except Exception as e:
        print(f"ERROR on {filename}: {e}")
        diseased_wrong += 1

print("\n" + "="*80)
print("FINAL RESULTS ON ALL XYZ IMAGES")
print("="*80)
print(f"\nHealthy Images ({len(healthy_files)} total):")
print(f"  ✓ Correct:   {healthy_correct}")
print(f"  ✗ Incorrect: {healthy_wrong}")
print(f"  Accuracy:  {100*healthy_correct/len(healthy_files):.1f}%")

print(f"\nDiseased Images ({len(diseased_files)} total):")
print(f"  ✓ Correct:   {diseased_correct}")
print(f"  ✗ Incorrect: {diseased_wrong}")
print(f"  Accuracy:  {100*diseased_correct/len(diseased_files):.1f}%")

total_correct = healthy_correct + diseased_correct
total = len(all_files)
print(f"\n{'='*80}")
print(f"OVERALL ACCURACY: {total_correct}/{total} = {100*total_correct/total:.1f}%")
print(f"{'='*80}\n")
