#!/usr/bin/env python3
"""
Test script to demonstrate the flowchart analysis API
"""
import requests
import os

# Path to sample flowchart
image_path = 'data/samples/sample_flowchart.png'

if not os.path.exists(image_path):
    print("❌ Sample flowchart not found. Generating...")
    os.system('python3 src/generate_test_data.py')

print("🚀 Testing Flowchart AI Evaluator API")
print("=" * 50)

# Open and send the image
with open(image_path, 'rb') as f:
    files = {'image': f}
    
    print(f"📤 Uploading: {image_path}")
    response = requests.post('http://localhost:5001/analyze', files=files)

if response.status_code == 200:
    data = response.json()
    
    print("\n✅ Analysis Complete!")
    print("=" * 50)
    print(f"\n📊 SCORE: {data['score']}/100")
    print(f"🔷 Shapes Detected: {data['shapes_detected']}")
    print(f"➡️  Arrows Detected: {data['arrows_detected']}")
    print(f"✓ Graph Valid: {data['graph_valid']}")
    
    print("\n📝 Generated Algorithm:")
    print("-" * 50)
    if isinstance(data['generated_algorithm'], list):
        for step in data['generated_algorithm']:
            print(f"  • {step}")
    else:
        print(f"  {data['generated_algorithm']}")
    
    print("\n💬 AI Feedback:")
    print("-" * 50)
    for i, feedback in enumerate(data['feedback'], 1):
        print(f"  {i}. {feedback}")
    
    print("\n" + "=" * 50)
    print("✨ Test completed successfully!")
    print(f"🌐 View in browser: http://localhost:5001")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
