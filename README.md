# AI-Assisted Flowchart Evaluation Prototype

## Overview

This is a **research prototype** for AI-assisted evaluation of student-drawn flowcharts. The system is designed as a **feasibility study** for academic research, demonstrating the potential of automated flowchart analysis while explicitly acknowledging its limitations.

## Problem Statement

Manual evaluation of student flowcharts is time-consuming and subjective. This prototype explores whether AI can assist teachers by:
- Extracting structure and logic from flowchart images
- Converting flowcharts to pseudo-algorithms
- Comparing student work with model solutions
- Providing partial, explainable marks

## System Architecture

```
┌─────────────┐
│ Image Input │
└──────┬──────┘
       │
┌──────▼──────────────┐
│ Image Processing    │  ← Shape & Arrow Detection
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Text Extraction     │  ← OCR & Normalization
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Graph Construction  │  ← Directed Graph
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Algorithm Gen       │  ← Pseudo-code
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Evaluation          │  ← Semantic Comparison
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Marks & Feedback    │
└─────────────────────┘
```

## Features

### 1. Image Processing Layer (`image_processor.py`)
- Detects flowchart symbols: Start/End (Oval), Process (Rectangle), Decision (Diamond)
- Uses heuristic-based shape classification
- Detects flow arrows using Hough Transform

### 2. Text Extraction Layer (`text_extractor.py`)
- OCR using Tesseract
- Text normalization (lowercasing, noise removal)
- Synonym mapping for common variations

### 3. Structural Representation (`graph_builder.py`)
- Converts flowchart to directed graph (NetworkX)
- Validates basic properties (start node, end node, DAG)

### 4. Algorithm Generation (`evaluator.py`)
- DFS traversal to generate pseudo-code
- Step-by-step algorithm extraction

### 5. Evaluation & Comparison (`evaluator.py`)
- TF-IDF + Cosine Similarity for semantic matching
- Partial marking based on step similarity
- Explainable feedback for each step

## Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR (optional, system uses mock OCR by default)

### Install Tesseract (Optional)
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

## Usage

### 1. Generate Sample Flowchart (Optional)
```bash
python3 src/generate_test_data.py
```

### 2. Run Evaluation

#### **Interactive Mode (Recommended)** 🆕
```bash
python3 src/main_interactive.py
```
This will prompt you to:
- Choose a flowchart image (sample or custom)
- Enter the model algorithm (correct answer)
- Get evaluation results

#### **Automated Mode**
```bash
python3 src/main.py
```
Uses hardcoded sample flowchart and model algorithm.

### 3. Debug Shape Detection
```bash
python3 src/debug_shapes.py
```

## Example Output

```
--- AI Flowchart Evaluation Prototype ---
Processing: data/samples/sample_flowchart.png
Detected 4 shapes and 39 arrows.
Built graph with 4 nodes and 3 edges.

--- RESULTS ---
Generated Algorithm:
  - Start/End: Start
  - Process: Input X
  - Decision: If X > 10
  - Start/End: Stop

Score: 50.0/100
Feedback:
  [x] Step 1 Correct: 'start' found.
  [x] Step 2 Missing: 'input value' not found.
  [x] Step 3 Missing: 'check if x is greater than 10' not found.
  [x] Step 4 Partial: 'stop' partially addressed.
```

## Project Structure

```
Flowchart-Eval/
├── src/
│   ├── image_processor.py      # Shape & arrow detection
│   ├── text_extractor.py       # OCR & normalization
│   ├── graph_builder.py        # Graph construction
│   ├── evaluator.py            # Pseudo-code generation & evaluation
│   ├── main.py                 # Main integration script
│   ├── generate_test_data.py   # Sample flowchart generator
│   └── debug_shapes.py         # Debug visualization
├── data/
│   └── samples/                # Sample flowcharts
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Limitations & Known Issues

### 1. Shape Detection
- **Heuristic-based**: Uses simple contour approximation, not deep learning
- **Clean images only**: Works best with digital/clean drawings
- **Limited symbols**: Only Start/End, Process, Decision
- **No loop detection**: Cannot handle complex loop structures

### 2. OCR Accuracy
- **Handwriting**: Poor performance on handwritten text
- **Requires Tesseract**: Mock OCR used by default for demo
- **No context**: Cannot infer meaning from illegible text

### 3. Graph Construction
- **Simple heuristics**: Uses vertical proximity, not true arrow following
- **No validation**: Doesn't check for flowchart correctness
- **Linear flows only**: Complex branching may fail

### 4. Evaluation
- **Semantic matching**: TF-IDF is basic, misses semantic equivalence
- **No partial credit logic**: Cannot recognize equivalent but differently worded steps
- **Fixed model**: Requires exact model algorithm format

### 5. General
- **Research prototype**: Not production-ready
- **No error handling**: Limited exception handling
- **No UI**: Command-line only

## Future Research Directions

1. **Deep Learning for Shape Detection**
   - Train YOLO/Faster R-CNN on flowchart datasets
   - Handle hand-drawn symbols more robustly

2. **Advanced OCR**
   - Fine-tune deep OCR models (TrOCR, PaddleOCR)
   - Context-aware text correction

3. **Semantic Understanding**
   - Use transformer models (BERT, GPT) for semantic comparison
   - Recognize equivalent logic expressed differently

4. **Complex Flow Handling**
   - Detect and evaluate loops (while, for)
   - Handle nested conditions

5. **Explainable AI**
   - Visualize differences between student and model
   - Provide actionable feedback for improvement

6. **Dataset Creation**
   - Collect real student flowcharts
   - Annotate for supervised learning

## Research Framing

This prototype is designed for **academic research** and should be presented as:
- A **feasibility study** exploring AI-assisted flowchart evaluation
- A **modular framework** for future research
- An **explainable system** prioritizing transparency over accuracy
- A **teacher assistance tool**, not a replacement for human grading

## Citation

If you use this prototype in your research, please cite:

```
[Your Research Paper]
AI-Assisted Evaluation of Student Flowcharts: A Feasibility Study
[Year]
```

## License

This is a research prototype. Please consult your institution's policies for usage and distribution.

## Contact

For questions or collaboration, please contact [Your Email/Institution].
