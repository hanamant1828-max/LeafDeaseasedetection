#!/usr/bin/env python3
"""
Comprehensive analysis of all images in xyz folder
"""
import os
from analysis import DiseaseAnalyzer
from PIL import Image
import numpy as np

analyzer = DiseaseAnalyzer()
print(f"Model loaded: {analyzer.model_loaded}\n")

xyz_dir = 'xyz'
all_files = sorted([f for f in os.listdir(xyz_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])

# Categorize by expected label
healthy_files = [f for f in all_files if f.startswith('healthy_')]
diseased_files = [f for f in all_files if not f.startswith('healthy_')]

print("="*80)
print(f"COMPREHENSIVE XYZ FOLDER ANALYSIS")
print("="*80)
print(f"Total images: {len(all_files)}")
print(f"Expected healthy: {len(healthy_files)}")
print(f"Expected diseased: {len(diseased_files)}")
print("="*80)

healthy_correct = 0
healthy_wrong = 0
diseased_correct = 0
diseased_wrong = 0

print("\n" + "="*80)
print("TESTING HEALTHY IMAGES")
print("="*80)

for filename in healthy_files[:15]:  # Test first 15
    filepath = os.path.join(xyz_dir, filename)
    
    try:
        # Get image info
        img = Image.open(filepath)
        
        # Analyze
        result = analyzer.analyze_image(filepath)
        predicted = result['disease']
        
        is_correct = predicted == 'healthy'
        if is_correct:
            healthy_correct += 1
            status = "✓"
        else:
            healthy_wrong += 1
            status = "✗"
        
        print(f"{status} {filename[:40]:40} -> {result['disease_name']:20} ({result['confidence']:.0f}%)")
        
    except Exception as e:
        print(f"ERROR on {filename}: {e}")

print("\n" + "="*80)
print("TESTING DISEASED IMAGES")
print("="*80)

for filename in diseased_files[:15]:  # Test first 15
    filepath = os.path.join(xyz_dir, filename)
    
    try:
        result = analyzer.analyze_image(filepath)
        predicted = result['disease']
        
        is_correct = predicted == 'diseased'
        if is_correct:
            diseased_correct += 1
            status = "✓"
        else:
            diseased_wrong += 1
            status = "✗"
        
        print(f"{status} {filename[:40]:40} -> {result['disease_name']:20} ({result['confidence']:.0f}%)")
        
    except Exception as e:
        print(f"ERROR on {filename}: {e}")

print("\n" + "="*80)
print("FINAL RESULTS")
print("="*80)
print(f"Healthy Images:")
print(f"  Correct:   {healthy_correct}")
print(f"  Incorrect: {healthy_wrong}")
if healthy_correct + healthy_wrong > 0:
    print(f"  Accuracy:  {100*healthy_correct/(healthy_correct+healthy_wrong):.1f}%")

print(f"\nDiseased Images:")
print(f"  Correct:   {diseased_correct}")
print(f"  Incorrect: {diseased_wrong}")
if diseased_correct + diseased_wrong > 0:
    print(f"  Accuracy:  {100*diseased_correct/(diseased_correct+diseased_wrong):.1f}%")

total_correct = healthy_correct + diseased_correct
total_wrong = healthy_wrong + diseased_wrong
if total_correct + total_wrong > 0:
    print(f"\nOverall Accuracy: {100*total_correct/(total_correct+total_wrong):.1f}%")

print("="*80)
