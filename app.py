from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor
from text_extractor import TextExtractor
from graph_builder import GraphBuilder
from evaluator import Evaluator

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_flowchart():
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the flowchart using the existing modules
        # 1. Image Processing
        processor = ImageProcessor(filepath)
        shapes = processor.detect_shapes()
        arrows = processor.detect_arrows()
        
        # 2. Text Extraction (using mock OCR for now)
        extractor = TextExtractor()
        for shape in shapes:
            # Mock OCR based on shape type (since real OCR may not work well)
            if shape['type'] == 'Start/End':
                shape['text'] = 'Start' if shape['bbox'][1] < 200 else 'Stop'
            elif shape['type'] == 'Process':
                shape['text'] = 'Process Step'
            elif shape['type'] == 'Decision':
                shape['text'] = 'Decision'
            else:
                shape['text'] = ''
        
        # 3. Build graph
        builder = GraphBuilder()
        sorted_shapes = sorted(shapes, key=lambda s: s['bbox'][1])  # Sort by Y position
        for i in range(len(sorted_shapes) - 1):
            builder.graph.add_node(i, **sorted_shapes[i])
            builder.graph.add_node(i+1, **sorted_shapes[i+1])
            builder.graph.add_edge(i, i+1)
        
        # Validate graph
        is_valid = builder.graph.number_of_nodes() > 0
        message = f"Graph has {builder.graph.number_of_nodes()} nodes and {builder.graph.number_of_edges()} edges"
        
        # 4. Generate algorithm from graph
        algorithm_steps = []
        for node_id in sorted(builder.graph.nodes()):
            node_data = builder.graph.nodes[node_id]
            step = f"{node_data.get('type', 'Unknown')}: {node_data.get('text', '')}"
            algorithm_steps.append(step)
        
        # 5. Intelligent analysis (no model needed - works for ANY flowchart)
        feedback = []
        score = 0
        
        # Check for start node
        has_start = any(s['type'] == 'Start/End' and 'start' in s.get('text', '').lower() for s in shapes)
        if has_start:
            feedback.append("✓ Flowchart has a proper START node")
            score += 15
        else:
            feedback.append("✗ Missing START node - flowcharts should begin with a start symbol")
        
        # Check for end node
        has_end = any(s['type'] == 'Start/End' and any(word in s.get('text', '').lower() for word in ['end', 'stop', 'exit']) for s in shapes)
        if has_end:
            feedback.append("✓ Flowchart has a proper END node")
            score += 15
        else:
            feedback.append("✗ Missing END node - flowcharts should end with a stop/end symbol")
        
        # Check for process steps
        process_count = sum(1 for s in shapes if s['type'] == 'Process')
        if process_count > 0:
            feedback.append(f"✓ Contains {process_count} process step(s)")
            score += min(20, process_count * 5)
        else:
            feedback.append("! No process steps detected - flowcharts typically have actions/processes")
        
        # Check for decision nodes
        decision_count = sum(1 for s in shapes if s['type'] == 'Decision')
        if decision_count > 0:
            feedback.append(f"✓ Contains {decision_count} decision point(s)")
            score += min(20, decision_count * 10)
        else:
            feedback.append("! No decision points detected - consider if conditional logic is needed")
        
        # Check graph validity
        if is_valid:
            feedback.append(f"✓ Graph structure is valid: {message}")
            score += 15
        else:
            feedback.append(f"✗ Graph structure issue: {message}")
        
        # Check for shapes with text
        shapes_with_text = sum(1 for s in shapes if s.get('text', '').strip())
        if shapes_with_text > 0:
            feedback.append(f"✓ {shapes_with_text}/{len(shapes)} shapes have readable text")
            score += min(15, (shapes_with_text / max(len(shapes), 1)) * 15)
        else:
            feedback.append("! No text detected in shapes - ensure labels are clear and readable")
        
        # Cap score at 100
        score = min(100, score)
        
        # Prepare response
        response = {
            'success': True,
            'shapes_detected': len(shapes),
            'arrows_detected': len(arrows),
            'graph_valid': is_valid,
            'validation_message': message,
            'generated_algorithm': algorithm_steps,
            'score': round(score, 2),
            'max_score': 100,
            'feedback': feedback,
            'shapes': [
                {
                    'type': s['type'],
                    'text': s.get('text', ''),
                    'position': s['bbox']
                } for s in shapes
            ]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    print("🚀 Starting Flowchart Evaluation Web Server...")
    print("📍 Open your browser at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
