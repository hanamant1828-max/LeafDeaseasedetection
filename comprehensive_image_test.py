import os
import sys
from analysis import DiseaseAnalyzer

def test_images():
    analyzer = DiseaseAnalyzer()
    
    print("=" * 80)
    print("COMPREHENSIVE IMAGE TESTING REPORT")
    print("=" * 80)
    print()
    
    # Test diseased images
    diseased_dir = 'test_images/diseased'
    healthy_dir = 'test_images/healthy'
    xyz_dir = 'xyz'
    
    all_results = {
        'diseased_correct': [],
        'diseased_wrong': [],
        'healthy_correct': [],
        'healthy_wrong': [],
        'xyz_diseased': [],
        'xyz_healthy': []
    }
    
    # Test diseased images
    print("\n" + "=" * 80)
    print("TESTING DISEASED IMAGES (Should detect as DISEASED)")
    print("=" * 80)
    
    if os.path.exists(diseased_dir):
        diseased_files = [f for f in os.listdir(diseased_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        for i, filename in enumerate(diseased_files, 1):
            filepath = os.path.join(diseased_dir, filename)
            try:
                result = analyzer.analyze_image(filepath)
                detected = result['disease']
                confidence = result['confidence']
                severity = result['severity']
                ml_powered = result['analysis_details']['ml_powered']
                
                if detected == 'diseased':
                    status = "✓ CORRECT"
                    all_results['diseased_correct'].append(filename)
                else:
                    status = "✗ WRONG"
                    all_results['diseased_wrong'].append(filename)
                
                print(f"{i}. {filename}")
                print(f"   Result: {result['disease_name']} | Confidence: {confidence:.1f}% | Severity: {severity}")
                print(f"   ML Model: {ml_powered} | Status: {status}")
                print()
                
            except Exception as e:
                print(f"{i}. {filename} - ERROR: {e}")
                print()
    
    # Test healthy images
    print("\n" + "=" * 80)
    print("TESTING HEALTHY IMAGES (Should detect as HEALTHY)")
    print("=" * 80)
    
    if os.path.exists(healthy_dir):
        healthy_files = [f for f in os.listdir(healthy_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        for i, filename in enumerate(healthy_files, 1):
            filepath = os.path.join(healthy_dir, filename)
            try:
                result = analyzer.analyze_image(filepath)
                detected = result['disease']
                confidence = result['confidence']
                ml_powered = result['analysis_details']['ml_powered']
                
                if detected == 'healthy':
                    status = "✓ CORRECT"
                    all_results['healthy_correct'].append(filename)
                else:
                    status = "✗ WRONG"
                    all_results['healthy_wrong'].append(filename)
                
                print(f"{i}. {filename}")
                print(f"   Result: {result['disease_name']} | Confidence: {confidence:.1f}%")
                print(f"   ML Model: {ml_powered} | Status: {status}")
                print()
                
            except Exception as e:
                print(f"{i}. {filename} - ERROR: {e}")
                print()
    
    # Test xyz directory (mixed images)
    print("\n" + "=" * 80)
    print("TESTING XYZ DIRECTORY IMAGES")
    print("=" * 80)
    
    if os.path.exists(xyz_dir):
        xyz_files = sorted([f for f in os.listdir(xyz_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])[:20]  # Test first 20
        for i, filename in enumerate(xyz_files, 1):
            filepath = os.path.join(xyz_dir, filename)
            try:
                result = analyzer.analyze_image(filepath)
                detected = result['disease']
                confidence = result['confidence']
                severity = result['severity']
                ml_powered = result['analysis_details']['ml_powered']
                
                expected = 'diseased' if 'diseased' in filename.lower() else 'healthy'
                
                if detected == expected:
                    status = "✓ CORRECT"
                else:
                    status = "✗ WRONG"
                
                if detected == 'diseased':
                    all_results['xyz_diseased'].append(filename)
                else:
                    all_results['xyz_healthy'].append(filename)
                
                print(f"{i}. {filename}")
                print(f"   Expected: {expected.upper()} | Detected: {result['disease_name']}")
                print(f"   Confidence: {confidence:.1f}% | Severity: {severity} | ML: {ml_powered}")
                print(f"   Status: {status}")
                print()
                
            except Exception as e:
                print(f"{i}. {filename} - ERROR: {e}")
                print()
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    
    total_diseased = len(all_results['diseased_correct']) + len(all_results['diseased_wrong'])
    total_healthy = len(all_results['healthy_correct']) + len(all_results['healthy_wrong'])
    
    print(f"\nDISEASED IMAGES:")
    print(f"  Total: {total_diseased}")
    print(f"  Correct: {len(all_results['diseased_correct'])} ({len(all_results['diseased_correct'])/max(total_diseased,1)*100:.1f}%)")
    print(f"  Wrong: {len(all_results['diseased_wrong'])} ({len(all_results['diseased_wrong'])/max(total_diseased,1)*100:.1f}%)")
    
    print(f"\nHEALTHY IMAGES:")
    print(f"  Total: {total_healthy}")
    print(f"  Correct: {len(all_results['healthy_correct'])} ({len(all_results['healthy_correct'])/max(total_healthy,1)*100:.1f}%)")
    print(f"  Wrong: {len(all_results['healthy_wrong'])} ({len(all_results['healthy_wrong'])/max(total_healthy,1)*100:.1f}%)")
    
    print(f"\nOVERALL ACCURACY:")
    total = total_diseased + total_healthy
    correct = len(all_results['diseased_correct']) + len(all_results['healthy_correct'])
    if total > 0:
        print(f"  {correct}/{total} = {correct/total*100:.1f}%")
    
    # List wrong predictions
    if all_results['diseased_wrong']:
        print(f"\n❌ DISEASED IMAGES INCORRECTLY DETECTED AS HEALTHY:")
        for filename in all_results['diseased_wrong']:
            print(f"   - {filename}")
    
    if all_results['healthy_wrong']:
        print(f"\n❌ HEALTHY IMAGES INCORRECTLY DETECTED AS DISEASED:")
        for filename in all_results['healthy_wrong']:
            print(f"   - {filename}")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    test_images()
