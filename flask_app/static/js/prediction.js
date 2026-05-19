// Advanced Interactive Prediction System - DiagnostiX
let selectedFile = null;
let currentDisease = 'brain';
const diseaseDescriptions = {
    brain: {
        title: 'Brain Tumor Detection',
        text: 'Upload an MRI scan to detect and classify brain tumors. Our deep learning model can identify glioma, meningioma, and pituitary tumors with high accuracy.'
    },
    xray: {
        title: 'Chest X-Ray Analysis',
        text: 'Upload a chest X-ray image to detect pneumonia and other lung diseases. Advanced CNN model trained on thousands of medical images.'
    },
    breast: {
        title: 'Breast Cancer Prediction',
        text: 'Answer health questions or upload clinical data to predict breast cancer risk. Based on comprehensive clinical metrics and machine learning.'
    },
    heart: {
        title: 'Heart Disease Prediction',
        text: 'Provide your cardiovascular metrics to assess heart disease risk. Integrated XGBoost model for accurate risk prediction.'
    },
    diabetes: {
        title: 'Diabetes Risk Assessment',
        text: 'Share your health metrics to evaluate diabetes risk. Advanced neural network trained on extensive patient health data.'
    }
};

const diseaseLoadingTexts = {
    brain: ["Analyzing MRI...", "Detecting Tumor Features...", "Running Deep Learning...", "Generating Report..."],
    xray: ["Analyzing X-Ray...", "Detecting Abnormalities...", "Running CNN Model...", "Preparing Report..."],
    breast: ["Processing Clinical Data...", "Running Classifier...", "Computing Risk Score...", "Finalizing Report..."],
    heart: ["Analyzing Heart Metrics...", "Computing Risk Factors...", "Running ML Model...", "Generating Assessment..."],
    diabetes: ["Processing Health Data...", "Analyzing Risk Factors...", "Computing Score...", "Preparing Report..."]
};

// Initialize disease selection
function selectDisease(disease) {
    currentDisease = disease;
    
    // Update active card
    document.querySelectorAll('.disease-selector-card').forEach(card => card.classList.remove('active'));
    document.querySelector(`[data-disease="${disease}"]`).classList.add('active');
    
    // Update description
    const desc = diseaseDescriptions[disease];
    document.getElementById('desc-title').textContent = desc.title;
    document.getElementById('desc-text').textContent = desc.text;
    
    // Hide all sections and show current
    const sections = ['brain', 'xray', 'breast', 'heart', 'diabetes'];
    sections.forEach(s => {
        const section = document.getElementById(`${s}-section`);
        if (section) {
            section.classList.remove('active');
            section.classList.add('hidden');
        }
    });
    
    const activeSection = document.getElementById(`${disease}-section`);
    if (activeSection) {
        activeSection.classList.add('active');
        activeSection.classList.remove('hidden');
    }
    
    // Reset file input and preview
    resetUploadZone(disease);
}

function resetUploadZone(disease) {
    const uploadArea = document.getElementById(`upload-area-${disease}`);
    const preview = document.getElementById(`preview-container-${disease}`);
    const fileInput = document.getElementById(`file-input-${disease}`);
    
    if (preview) preview.classList.add('hidden');
    if (uploadArea) uploadArea.classList.remove('hidden');
    if (fileInput) fileInput.value = '';
    selectedFile = null;
}

// Setup file upload for image-based diseases
function setupImageUpload(disease) {
    const zone = document.getElementById(`upload-area-${disease}`);
    const input = document.getElementById(`file-input-${disease}`);
    
    if (!zone || !input) return;

    zone.addEventListener('click', () => input.click());
    zone.addEventListener('dragover', e => { 
        e.preventDefault(); 
        zone.classList.add('dragover'); 
    });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', e => {
        e.preventDefault();
        zone.classList.remove('dragover');
        handleFile(e.dataTransfer.files[0], disease);
    });
    input.onchange = () => handleFile(input.files[0], disease);
}

function handleFile(file, disease) {
    if (!file || !file.type.startsWith('image/')) {
        alert('Please upload a valid image file (JPG, PNG)');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }
    
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = e => {
        document.getElementById(`image-preview-${disease}`).src = e.target.result;
        document.getElementById(`preview-container-${disease}`).classList.remove('hidden');
        document.getElementById(`upload-area-${disease}`).classList.add('hidden');
    };
    reader.readAsDataURL(file);
}

// Heart Disease specific functions
function showHeartOption(option) {
    document.querySelectorAll('#heart-section .tab-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');
    
    document.getElementById('heart-csv').classList.add('hidden');
    document.getElementById('heart-questionnaire').classList.add('hidden');
    
    if (option === 'csv') {
        document.getElementById('heart-csv').classList.remove('hidden');
    } else {
        document.getElementById('heart-questionnaire').classList.remove('hidden');
    }
}

function setupHeartSliders() {
    const sliders = [
        { id: 'heart-age', display: 'heart-age-v' },
        { id: 'heart-chol', display: 'heart-chol-v' },
        { id: 'heart-bp', display: 'heart-bp-v' },
        { id: 'heart-hr', display: 'heart-hr-v' },
        { id: 'heart-maxhr', display: 'heart-maxhr-v' },
        { id: 'heart-st', display: 'heart-st-v' }
    ];
    
    sliders.forEach(item => {
        const slider = document.getElementById(item.id);
        if (slider) {
            slider.oninput = () => {
                document.getElementById(item.display).textContent = parseFloat(slider.value).toFixed(1);
            };
        }
    });
}

// Diabetes specific functions
function showDiabetesOption(option) {
    document.querySelectorAll('#diabetes-section .tab-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');
    
    document.getElementById('diabetes-csv').classList.add('hidden');
    document.getElementById('diabetes-questionnaire').classList.add('hidden');
    
    if (option === 'csv') {
        document.getElementById('diabetes-csv').classList.remove('hidden');
    } else {
        document.getElementById('diabetes-questionnaire').classList.remove('hidden');
    }
}

function setupDiabetesSliders() {
    const sliders = [
        { id: 'diab-age', display: 'diab-age-v' },
        { id: 'diab-preg', display: 'diab-preg-v' },
        { id: 'diab-glucose', display: 'diab-glucose-v' },
        { id: 'diab-bp', display: 'diab-bp-v' },
        { id: 'diab-bmi', display: 'diab-bmi-v' },
        { id: 'diab-insulin', display: 'diab-insulin-v' }
    ];
    
    sliders.forEach(item => {
        const slider = document.getElementById(item.id);
        if (slider) {
            slider.oninput = () => {
                document.getElementById(item.display).textContent = parseFloat(slider.value).toFixed(1);
            };
        }
    });
}

// Start prediction for image-based and csv files
async function startPrediction(disease) {
    if (!selectedFile) {
        if (disease === 'heart' || disease === 'diabetes') {
            const inputType = document.getElementById(`${disease}-csv`).classList.contains('hidden') ? 'questionnaire' : 'csv';
            if (inputType === 'csv') {
                const csvInput = document.getElementById(`csv-input-${disease}`);
                if (csvInput && csvInput.files.length > 0) {
                    selectedFile = csvInput.files[0];
                } else {
                    alert('Please select a file first');
                    return;
                }
            } else {
                return;
            }
        } else {
            alert('Please select an image first');
            return;
        }
    }
    
    const loading = document.getElementById('loading-screen');
    loading.classList.remove('hidden');

    const texts = diseaseLoadingTexts[disease];
    let i = 0;
    const interval = setInterval(() => {
        document.getElementById('loading-text').innerText = texts[i % texts.length];
        i++;
    }, 800);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('disease', disease);

    try {
        const res = await fetch('/api/predict', { 
            method: 'POST', 
            body: formData 
        });
        
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const data = await res.json();
        clearInterval(interval);
        loading.classList.add('hidden');
        showResults(data, disease);
    } catch (err) {
        clearInterval(interval);
        loading.classList.add('hidden');
        console.error('Prediction error:', err);
        alert('Prediction failed: ' + err.message);
    }
}

// Submit questionnaire for tabular data diseases
async function submitQuestionnaire(disease) {
    const loading = document.getElementById('loading-screen');
    loading.classList.remove('hidden');

    const texts = diseaseLoadingTexts[disease];
    let i = 0;
    const interval = setInterval(() => {
        document.getElementById('loading-text').innerText = texts[i % texts.length];
        i++;
    }, 800);

    // Collect form data based on disease
    let formData = new FormData();
    
    if (disease === 'heart') {
        formData.append('age', document.getElementById('heart-age')?.value || '');
        formData.append('chol', document.getElementById('heart-chol')?.value || '');
        formData.append('bp', document.getElementById('heart-bp')?.value || '');
        formData.append('hr', document.getElementById('heart-hr')?.value || '');
        formData.append('maxhr', document.getElementById('heart-maxhr')?.value || '');
        formData.append('st', document.getElementById('heart-st')?.value || '');
    } else if (disease === 'diabetes') {
        formData.append('age', document.getElementById('diab-age')?.value || '');
        formData.append('preg', document.getElementById('diab-preg')?.value || '');
        formData.append('glucose', document.getElementById('diab-glucose')?.value || '');
        formData.append('bp', document.getElementById('diab-bp')?.value || '');
        formData.append('bmi', document.getElementById('diab-bmi')?.value || '');
        formData.append('insulin', document.getElementById('diab-insulin')?.value || '');
    }
    
    formData.append('disease', disease);

    try {
        const res = await fetch('/api/predict', { 
            method: 'POST', 
            body: formData 
        });
        
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const data = await res.json();
        clearInterval(interval);
        loading.classList.add('hidden');
        showResults(data, disease);
    } catch (err) {
        clearInterval(interval);
        loading.classList.add('hidden');
        console.error('Prediction error:', err);
        alert('Prediction failed: ' + err.message);
    }
}

// Display results in a beautiful card
function showResults(data, disease) {
    const container = document.getElementById('result-card');
    const conf = parseFloat(data.confidence || 0);
    
    let diseaseLabel = {
        brain: 'Brain Tumor',
        xray: 'Chest X-Ray',
        breast: 'Breast Cancer',
        heart: 'Heart Disease',
        diabetes: 'Diabetes Risk'
    }[disease];
    
    // Determine result color based on prediction
    let resultColor = conf > 0.7 ? '#ef4444' : '#10b981';
    let resultClass = conf > 0.7 ? 'high-risk' : 'low-risk';
    
    container.innerHTML = `
        <div class="result-content">
            <div class="result-header">
                <h2>✅ Analysis Complete</h2>
                <span class="disease-result-badge">${diseaseLabel}</span>
            </div>
            
            <div class="prediction-display ${resultClass}">
                <div class="prediction-label">Prediction</div>
                <div class="prediction-value">${data.prediction}</div>
            </div>
            
            <div class="confidence-box">
                <div class="conf-label">Confidence Score</div>
                <div class="conf-value">${(conf * 100).toFixed(1)}%</div>
                <div class="progress-bar-container">
                    <div class="progress-bar"><div class="progress-fill" style="width: ${conf*100}%; background: ${resultColor};"></div></div>
                </div>
            </div>
            
            ${data.class_probabilities ? `
                <div class="probabilities-box">
                    <h4>Class Probabilities</h4>
                    <div class="prob-grid">
                        ${Object.entries(data.class_probabilities).map(([k,v]) => `
                            <div class="prob-item">
                                <span class="prob-label">${k}</span>
                                <div class="prob-bar-container">
                                    <div class="prob-bar"><div class="prob-fill" style="width: ${v*100}%"></div></div>
                                </div>
                                <span class="prob-percent">${(v*100).toFixed(1)}%</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            <div class="result-metadata">
                <span>⏱️ Processing Time: ${data.processing_time || '0.2s'}</span>
            </div>
            
            <div class="result-actions">
                <button onclick="location.reload()" class="btn-primary">New Analysis</button>
                <button onclick="selectDisease('brain')" class="btn-secondary">Try Another Test</button>
            </div>
        </div>
    `;
    
    container.classList.remove('hidden');
    container.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Save to history
    const prediction = {
        disease: disease,
        prediction: data.prediction,
        confidence: conf,
        timestamp: new Date().toISOString()
    };
    savePredictionHistory(prediction);
}

// Local storage management for prediction history
function savePredictionHistory(prediction) {
    try {
        let history = JSON.parse(localStorage.getItem('predictionHistory') || '[]');
        history.unshift(prediction);
        history = history.slice(0, 20); // Keep last 20
        localStorage.setItem('predictionHistory', JSON.stringify(history));
    } catch (err) {
        console.error('Failed to save history:', err);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Setup image uploads for image-based diseases
    ['brain', 'xray', 'breast'].forEach(disease => setupImageUpload(disease));
    
    // Setup sliders for tabular diseases
    setupHeartSliders();
    setupDiabetesSliders();
    
    // Initialize with brain tumor selected
    selectDisease('brain');
});