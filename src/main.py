
import sys
import os
from image_processor import ImageProcessor
from text_extractor import TextExtractor
from graph_builder import GraphBuilder
from evaluator import Evaluator

def main(image_path, model_algorithm, mock_ocr=True):
    print(f"--- AI Flowchart Evaluation Prototype ---")
    print(f"Processing: {image_path}")

    # 1. Image Processing
    proc = ImageProcessor(image_path)
    shapes = proc.detect_shapes()
    arrows = proc.detect_arrows()
    print(f"Detected {len(shapes)} shapes and {len(arrows)} arrows.")

    # 2. Text Extraction (with optional Mock for demonstration)
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
    # Simple heuristic for edges: vertical proximity for this linear demo
    sorted_shapes = sorted(shapes, key=lambda s: s['bbox'][1])
    for i in range(len(sorted_shapes) - 1):
        builder.graph.add_node(i, **sorted_shapes[i])
        builder.graph.add_node(i+1, **sorted_shapes[i+1])
        builder.graph.add_edge(i, i+1)
    
    print(f"Built graph with {builder.graph.number_of_nodes()} nodes and {builder.graph.number_of_edges()} edges.")

    # 4. Evaluation
    evaluator = Evaluator(builder.graph, model_algorithm)
    student_steps = evaluator.generate_pseudo_code()
    score, feedback = evaluator.evaluate(student_steps)

    print("\n--- RESULTS ---")
    print(f"Generated Algorithm:\n" + "\n".join(f"  - {step}" for step in student_steps))
    print(f"\nScore: {score}/100")
    print("Feedback:")
    for f in feedback:
        print(f"  [x] {f}")

if __name__ == "__main__":
    sample_img = "data/samples/sample_flowchart.png"
    if not os.path.exists(sample_img):
        print("Please run 'python src/generate_test_data.py' first.")
        sys.exit(1)
        
    model_algo = [
        "start",
        "input value",
        "check if x is greater than 10",
        "stop"
    ]
    
    main(sample_img, model_algo)
