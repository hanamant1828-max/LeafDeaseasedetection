import os
from PIL import Image
import numpy as np
from analysis import DiseaseAnalyzer

def inspect_image(filepath):
    """Detailed inspection of an image"""
    print(f"\n{'='*80}")
    print(f"INSPECTING: {filepath}")
    print(f"{'='*80}")
    
    try:
        img = Image.open(filepath)
        print(f"Image size: {img.size}")
        print(f"Image mode: {img.mode}")
        
        # Get pixel statistics
        pixels = np.array(img.convert('RGB'))
        print(f"\nPixel value ranges:")
        print(f"  Red:   min={pixels[:,:,0].min()}, max={pixels[:,:,0].max()}, mean={pixels[:,:,0].mean():.1f}")
        print(f"  Green: min={pixels[:,:,1].min()}, max={pixels[:,:,1].max()}, mean={pixels[:,:,1].mean():.1f}")
        print(f"  Blue:  min={pixels[:,:,2].min()}, max={pixels[:,:,2].max()}, mean={pixels[:,:,2].mean():.1f}")
        
        # Run analysis
        analyzer = DiseaseAnalyzer()
        result = analyzer.analyze_image(filepath)
        
        print(f"\n{'='*80}")
        print(f"ANALYSIS RESULT:")
        print(f"{'='*80}")
        print(f"Disease: {result['disease_name']}")
        print(f"Confidence: {result['confidence']:.1f}%")
        print(f"Severity: {result['severity']}")
        
        print(f"\nDetailed Analysis:")
        details = result['analysis_details']
        print(f"  Green content: {details['green_content']:.2f}%")
        print(f"  Brown content: {details['brown_content']:.2f}%")
        print(f"  Yellow content: {details['yellow_content']:.2f}%")
        print(f"  Spots detected: {details['spots_detected']:.2f}%")
        print(f"  Overall health: {details['overall_health']:.2f}")
        print(f"  ML powered: {details['ml_powered']}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Inspect the two problematic images
    wrong_images = [
        'xyz/diseased_plant_leave_e073f745.jpg',
        'xyz/diseased_plant_leave_e958da4b.jpg'
    ]
    
    for img_path in wrong_images:
        if os.path.exists(img_path):
            inspect_image(img_path)
        else:
            print(f"File not found: {img_path}")
    
    # For comparison, inspect a correctly detected diseased image
    print("\n\n" + "="*80)
    print("FOR COMPARISON - A CORRECTLY DETECTED DISEASED IMAGE:")
    print("="*80)
    inspect_image('xyz/diseased_plant_leave_199dde3b.jpg')
