// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const removeBtn = document.getElementById('removeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadSection = document.getElementById('uploadSection');
const resultsSection = document.getElementById('resultsSection');
const loadingOverlay = document.getElementById('loadingOverlay');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

// State
let selectedFile = null;

// Event Listeners
uploadArea.addEventListener('click', (e) => {
    e.preventDefault();
    fileInput.click();
});

uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
removeBtn.addEventListener('click', resetUpload);
analyzeBtn.addEventListener('click', analyzeFlowchart);
newAnalysisBtn.addEventListener('click', resetAll);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    console.log('File selected:', file.name, file.type, file.size);

    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
        alert('Please upload a PNG or JPEG image');
        return;
    }

    // Validate file size (max 16MB)
    if (file.size > 16 * 1024 * 1024) {
        alert('File size must be less than 16MB');
        return;
    }

    selectedFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    imagePreview.src = '';
    uploadArea.style.display = 'block';
    previewContainer.style.display = 'none';
}

function resetAll() {
    resetUpload();
    uploadSection.style.display = 'block';
    resultsSection.style.display = 'none';
}

async function analyzeFlowchart() {
    if (!selectedFile) {
        alert('Please upload a flowchart image first');
        return;
    }

    // Show loading
    loadingOverlay.style.display = 'flex';

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedFile);

        console.log('Sending request to analyze...');

        // Send request to backend
        const response = await fetch('http://localhost:5001/analyze', {
            method: 'POST',
            body: formData
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Analysis failed');
        }

        const data = await response.json();
        console.log('Response data:', data);

        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze flowchart: ' + error.message);
    } finally {
        loadingOverlay.style.display = 'none';
    }
}

function displayResults(data) {
    // Hide upload section, show results
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'block';

    // Update score
    const score = data.score;
    document.getElementById('scoreValue').textContent = Math.round(score);

    // Animate score ring
    const circumference = 2 * Math.PI * 70;
    const offset = circumference - (score / 100) * circumference;

    // Add gradient definition to SVG
    const svg = document.querySelector('.score-ring');
    if (!svg.querySelector('#scoreGradient')) {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'scoreGradient');
        gradient.setAttribute('x1', '0%');
        gradient.setAttribute('y1', '0%');
        gradient.setAttribute('x2', '100%');
        gradient.setAttribute('y2', '100%');

        const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop1.setAttribute('offset', '0%');
        stop1.setAttribute('stop-color', '#667eea');

        const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop2.setAttribute('offset', '100%');
        stop2.setAttribute('stop-color', '#764ba2');

        gradient.appendChild(stop1);
        gradient.appendChild(stop2);
        defs.appendChild(gradient);
        svg.appendChild(defs);
    }

    setTimeout(() => {
        document.getElementById('scoreRing').style.strokeDashoffset = offset;
    }, 100);

    // Update stats
    document.getElementById('shapesCount').textContent = data.shapes_detected;
    document.getElementById('arrowsCount').textContent = data.arrows_detected;
    document.getElementById('graphValid').textContent = data.graph_valid ? '✓ Yes' : '✗ No';

    // Update algorithm output
    const algorithmOutput = document.getElementById('algorithmOutput');
    if (Array.isArray(data.generated_algorithm)) {
        algorithmOutput.textContent = data.generated_algorithm.join('\n');
    } else {
        algorithmOutput.textContent = data.generated_algorithm;
    }

    // Update feedback
    const feedbackList = document.getElementById('feedbackList');
    feedbackList.innerHTML = '';

    if (data.feedback && data.feedback.length > 0) {
        data.feedback.forEach((item, index) => {
            const feedbackItem = createFeedbackItem(item, index + 1);
            feedbackList.appendChild(feedbackItem);
        });
    } else {
        feedbackList.innerHTML = '<p style="color: var(--text-secondary);">No detailed feedback available.</p>';
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function createFeedbackItem(feedback, index) {
    const div = document.createElement('div');

    // Determine feedback type based on icon
    let type = 'missing';
    let icon = '!';

    if (feedback.startsWith('✓')) {
        type = 'correct';
        icon = '✓';
    } else if (feedback.startsWith('✗')) {
        type = 'missing';
        icon = '✗';
    } else if (feedback.startsWith('!')) {
        type = 'partial';
        icon = '!';
    }

    div.className = `feedback-item ${type}`;
    div.innerHTML = `
        <div class="feedback-icon">${icon}</div>
        <div class="feedback-text">${feedback}</div>
    `;

    return div;
}

// Add smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';

console.log('Script loaded successfully');
