from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import urllib.request
import urllib.error

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    print("--- /evaluate called ---")
    data = request.json
    api_key = data.get('api_key', '').strip()
    question = data.get('question', '').strip()
    rubric = data.get('rubric', '').strip()
    image_base64 = data.get('image_base64', '').strip()
    image_mime = data.get('image_mime', 'image/jpeg')

    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    if not question:
        return jsonify({'error': 'Exam question is required'}), 400
    if not image_base64:
        return jsonify({'error': 'Flowchart image is required'}), 400

    print(f"Question: {question[:50]}")

    prompt = f"""You are an expert academic evaluator for computer science flowcharts.

Exam Question: {question}

Marking Rubric:
{rubric if rubric else 'Use standard academic flowchart evaluation criteria covering: algorithmic correctness, correct use of flowchart symbols (oval=start/stop, rectangle=process, diamond=decision, parallelogram=input/output), flow clarity and logic, and presentation/neatness. Total marks: 10.'}

Analyze the flowchart image carefully:
- Read all text inside shapes even if handwritten
- Identify every symbol (ovals, rectangles, diamonds, parallelograms, arrows)
- Trace the logical flow step by step
- Compare against the correct algorithm for the given question

Respond ONLY with a valid JSON object, no markdown, no extra text:
{{
  "categories": [
    {{"name": "Category Name", "scored": 3.5, "max": 4, "comment": "Brief specific feedback"}},
    {{"name": "Category Name", "scored": 2, "max": 3, "comment": "Brief specific feedback"}}
  ],
  "total_scored": 8.5,
  "total_max": 10,
  "overall_feedback": "2-3 sentence overall assessment with specific observations from the flowchart",
  "improvements": "Specific actionable improvements the student can make to get full marks"
}}"""

    payload = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": image_mime, "data": image_base64}},
                {"text": prompt}
            ]
        }],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 4096}
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    try:
        print("Calling Gemini API...")
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'x-goog-api-key': api_key
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))

        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"Full response:\n{text}")

        # Extract JSON from response robustly
        import re
        # Try to find JSON block between curly braces
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            clean = match.group(0)
        else:
            clean = text.replace('```json', '').replace('```', '').strip()

        return jsonify(json.loads(clean))

    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {body}")
        try:
            msg = json.loads(body).get('error', {}).get('message', body)
        except:
            msg = body
        return jsonify({'error': f'Gemini API error: {msg}'}), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Flowchart Evaluator running at http://localhost:8080")
    print("Powered by: Google Gemini (FREE - 1500 requests/day)")
    app.run(debug=True, port=8080)