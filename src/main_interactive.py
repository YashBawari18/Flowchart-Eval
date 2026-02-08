
import sys
import os
from image_processor import ImageProcessor
from text_extractor import TextExtractor
from graph_builder import GraphBuilder
from evaluator import Evaluator

# Predefined model algorithm (correct answer)
MODEL_ALGORITHM = [
    "start",
    "input value",
    "check if x is greater than 10",
    "stop"
]

def analyze_and_evaluate(image_path, mock_ocr=True):
    """Analyze flowchart and evaluate against model algorithm."""
    print(f"\n{'='*60}")
    print(f"🔍 Analyzing Flowchart...")
    print(f"{'='*60}")
    print(f"Processing: {image_path}\n")

    # 1. Image Processing
    proc = ImageProcessor(image_path)
    shapes = proc.detect_shapes()
    arrows = proc.detect_arrows()
    print(f"📊 Detected {len(shapes)} shapes and {len(arrows)} arrows.")

    # 2. Text Extraction
    extractor = TextExtractor()
    for shape in shapes:
        if mock_ocr:
            # Simulated OCR based on shape type for demonstration
            if shape['type'] == 'Start/End':
                shape['text'] = 'Start' if shape['bbox'][1] < 200 else 'Stop'
            elif shape['type'] == 'Process':
                shape['text'] = 'Input X'
            elif shape['type'] == 'Decision':
                shape['text'] = 'If X > 10'
        else:
            shape['text'] = extractor.extract_text(proc.image, shape['bbox'])
    
    # 3. Graph Building
    builder = GraphBuilder()
    sorted_shapes = sorted(shapes, key=lambda s: s['bbox'][1])
    for i in range(len(sorted_shapes) - 1):
        builder.graph.add_node(i, **sorted_shapes[i])
        builder.graph.add_node(i+1, **sorted_shapes[i+1])
        builder.graph.add_edge(i, i+1)
    
    print(f"🔗 Built graph with {builder.graph.number_of_nodes()} nodes and {builder.graph.number_of_edges()} edges.")

    # 4. Generate algorithm from flowchart
    evaluator = Evaluator(builder.graph, MODEL_ALGORITHM)
    student_steps = evaluator.generate_pseudo_code()
    
    print(f"\n{'='*60}")
    print("✅ Analysis Complete!")
    print(f"{'='*60}")
    print(f"\n📝 Extracted Algorithm from Your Flowchart:")
    for i, step in enumerate(student_steps, 1):
        print(f"  {i}. {step}")
    
    # 5. Evaluate
    score, feedback = evaluator.evaluate(student_steps)

    print(f"\n{'='*60}")
    print("📊 EVALUATION RESULTS")
    print(f"{'='*60}")
    
    print(f"\n🎯 Expected Algorithm (Correct Answer):")
    for i, step in enumerate(MODEL_ALGORITHM, 1):
        print(f"  {i}. {step}")
    
    print(f"\n{'='*60}")
    print(f"🏆 Final Score: {score}/100")
    print(f"{'='*60}")
    
    print("\n💬 Detailed Feedback:")
    for f in feedback:
        print(f"  • {f}")
    print(f"\n{'='*60}\n")

def get_image_path():
    """Get flowchart image path from user."""
    print("\n" + "="*60)
    print("🎓 AI-Assisted Flowchart Evaluation System")
    print("="*60)
    
    print("\n📁 Provide Your Flowchart Image")
    print("-" * 60)
    print("Options:")
    print("  1. Use sample flowchart (auto-generated)")
    print("  2. Enter custom image path")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        image_path = "data/samples/sample_flowchart.png"
        if not os.path.exists(image_path):
            print("\n⚠️  Sample flowchart not found!")
            print("Generating sample flowchart...")
            os.system("python3 src/generate_test_data.py")
        print(f"✅ Using: {image_path}")
    else:
        image_path = input("\nEnter the path to your flowchart image: ").strip()
        if not os.path.exists(image_path):
            print(f"\n❌ Error: File not found: {image_path}")
            sys.exit(1)
        print(f"✅ Image loaded: {image_path}")
    
    return image_path

if __name__ == "__main__":
    try:
        # Get image path from user
        image_path = get_image_path()
        
        # Analyze and evaluate automatically
        analyze_and_evaluate(image_path)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
