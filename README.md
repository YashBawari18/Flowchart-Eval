# Flowchart Evaluator — Setup Guide

## Step 1: Install Python
Make sure Python 3.8+ is installed. Download from https://python.org if needed.

## Step 2: Install dependencies
Open terminal/command prompt in this folder and run:
```
pip install -r requirements.txt
```

## Step 3: Run the app
```
python app.py
```

## Step 4: Open in browser
Go to: http://localhost:5000

## Step 5: Use the app
1. Paste your Claude API key (get from https://console.anthropic.com)
2. Type the exam question
3. Paste the marking rubric
4. Upload a photo of the student's flowchart
5. Click "Evaluate Flowchart"

## Notes
- Your API key is never stored — it's only used to call Anthropic's API
- Works with handwritten AND printed flowcharts
- Any question/rubric can be used — fully dynamic evaluation
