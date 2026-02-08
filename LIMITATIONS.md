# Limitations and Failure Cases

## Purpose
This document explicitly outlines the limitations, assumptions, and known failure cases of the AI Flowchart Evaluation prototype. This transparency is essential for academic research and honest evaluation of the system's capabilities.

## Core Assumptions

### 1. Input Quality
- **Assumption**: Flowcharts are moderately clean (digital or neat hand-drawn)
- **Reality**: Messy handwriting, poor lighting, or low-resolution images will fail
- **Impact**: Shape detection accuracy drops below 50% with poor input quality

### 2. Symbol Set
- **Assumption**: Only Start/End, Process, and Decision symbols
- **Reality**: Real flowcharts use Input/Output, Predefined Process, Connectors, etc.
- **Impact**: Unrecognized symbols are ignored or misclassified

### 3. Flow Structure
- **Assumption**: Linear or simple branching flows
- **Reality**: Complex loops, nested conditions, and parallel flows exist
- **Impact**: Graph construction fails or produces incorrect topology

### 4. Text Legibility
- **Assumption**: Text is readable by OCR
- **Reality**: Handwritten text, cursive, or stylized fonts are illegible
- **Impact**: Empty or incorrect text extraction leads to wrong evaluation

## Known Failure Cases

### 1. Shape Detection Failures

#### Case 1.1: Overlapping Shapes
**Description**: When shapes overlap or touch, they may be detected as a single contour.

**Example**:
```
┌─────┐
│  A  │──┐
└─────┘  │  ┌─────┐
         └──│  B  │
            └─────┘
```
**Result**: Detected as one merged shape
**Workaround**: None in current implementation

#### Case 1.2: Irregular Shapes
**Description**: Hand-drawn shapes with wobbly lines may not match expected vertex counts.

**Example**: A hand-drawn diamond with 5-6 vertices instead of 4
**Result**: Misclassified as Start/End (oval)
**Workaround**: Adjust `approxPolyDP` epsilon parameter

#### Case 1.3: Very Small or Large Shapes
**Description**: Shapes outside the area threshold (1000-40000 pixels) are filtered out.

**Example**: Tiny annotation boxes or very large title boxes
**Result**: Ignored completely
**Workaround**: Adjust area thresholds in `image_processor.py`

### 2. OCR Failures

#### Case 2.1: Handwritten Text
**Description**: Tesseract OCR performs poorly on handwriting.

**Example**: "Input X" written in cursive → "Inpuf 7"
**Result**: Incorrect text leads to failed semantic matching
**Workaround**: Use deep OCR models (TrOCR, PaddleOCR)

#### Case 2.2: Special Characters
**Description**: Mathematical symbols, arrows in text, or special operators.

**Example**: "X ← 5" → "X 5"
**Result**: Lost semantic meaning
**Workaround**: Custom preprocessing for mathematical notation

#### Case 2.3: Multi-line Text
**Description**: Text spanning multiple lines in a single shape.

**Example**:
```
┌─────────┐
│ Read X  │
│ Read Y  │
└─────────┘
```
**Result**: May be read as "ReadXReadY" or split incorrectly
**Workaround**: Better ROI segmentation

### 3. Graph Construction Failures

#### Case 3.1: Crossing Arrows
**Description**: Arrows that cross without connecting.

**Example**:
```
A → B
  ╳
C → D
```
**Result**: False connections detected
**Workaround**: Implement proper arrow endpoint detection

#### Case 3.2: Bidirectional Flows
**Description**: Arrows going both directions (loops).

**Example**: `A ⇄ B`
**Result**: Only one direction detected or cycle in DAG validation fails
**Workaround**: Remove DAG constraint for loop support

#### Case 3.3: Multiple Start/End Nodes
**Description**: Flowcharts with multiple entry or exit points.

**Example**: Two "Start" nodes for different scenarios
**Result**: Validation fails or only one path is traversed
**Workaround**: Support multi-root graphs

### 4. Evaluation Failures

#### Case 4.1: Semantic Equivalence
**Description**: Different wording for the same logic.

**Example**:
- Model: "Check if X is greater than 10"
- Student: "Is X > 10?"
**Result**: Low similarity score despite being equivalent
**Workaround**: Use semantic embeddings (BERT, Sentence-BERT)

#### Case 4.2: Reordered Steps
**Description**: Correct logic but different step order.

**Example**:
- Model: [Input X, Input Y, Sum = X + Y]
- Student: [Input Y, Input X, Sum = X + Y]
**Result**: Steps marked as missing/incorrect
**Workaround**: Implement order-invariant comparison

#### Case 4.3: Variable Renaming
**Description**: Using different variable names.

**Example**:
- Model: "Input X"
- Student: "Input num"
**Result**: Marked as different despite same intent
**Workaround**: Variable normalization or symbolic execution

### 5. System-Level Failures

#### Case 5.1: No Tesseract Installation
**Description**: System requires Tesseract for OCR.

**Example**: Running on a system without Tesseract
**Result**: OCR fails, system uses mock data
**Workaround**: Provide mock OCR mode (currently implemented)

#### Case 5.2: Image Format Issues
**Description**: Unsupported image formats or corrupted files.

**Example**: HEIC, WebP, or damaged PNG files
**Result**: OpenCV fails to read image
**Workaround**: Convert to standard formats (PNG, JPG)

#### Case 5.3: Memory Constraints
**Description**: Very large images (>10MB) may cause memory issues.

**Example**: High-resolution scanned documents
**Result**: Slow processing or crash
**Workaround**: Resize images before processing

## Quantitative Performance Estimates

Based on testing with the sample flowchart:

| Metric | Performance | Notes |
|--------|-------------|-------|
| Shape Detection Accuracy | ~80% | Clean digital images |
| Shape Detection Accuracy | ~40% | Hand-drawn images |
| OCR Accuracy (Digital) | ~90% | With Tesseract |
| OCR Accuracy (Handwritten) | ~30% | With Tesseract |
| Graph Construction Accuracy | ~70% | Simple linear flows |
| Semantic Matching Accuracy | ~50% | TF-IDF based |
| Overall System Accuracy | ~40-60% | End-to-end |

**Note**: These are rough estimates based on limited testing. Formal evaluation requires a labeled dataset.

## Recommendations for Future Work

### Short-term Improvements
1. **Better Shape Detection**: Use template matching or simple CNN
2. **Improved OCR**: Integrate deep OCR models
3. **Robust Graph Construction**: Implement proper arrow following
4. **Enhanced Evaluation**: Use semantic embeddings

### Long-term Research
1. **Dataset Creation**: Collect and annotate real student flowcharts
2. **End-to-End Deep Learning**: Train a model to directly map images to algorithms
3. **Interactive Feedback**: Allow teachers to correct and retrain the system
4. **Multi-modal Learning**: Combine visual and textual understanding

## Conclusion

This prototype demonstrates **feasibility** but is **not production-ready**. It should be used as:
- A **research baseline** for comparison with future methods
- A **modular framework** for experimentation
- A **proof-of-concept** for AI-assisted grading

The documented limitations are intentional and serve to:
- Set realistic expectations
- Guide future research directions
- Ensure ethical use in educational settings

## References

1. Tesseract OCR: https://github.com/tesseract-ocr/tesseract
2. OpenCV Shape Detection: https://docs.opencv.org/
3. NetworkX Graph Library: https://networkx.org/
4. TF-IDF for Text Similarity: https://scikit-learn.org/

---

**Last Updated**: January 2026
**Version**: 1.0 (Research Prototype)
