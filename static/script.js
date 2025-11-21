// Global state
let currentTechnique = '';
let currentOperation = 'E';

// DOM Elements
const techniqueSelect = document.getElementById('techniqueSelect');
const techniqueInfo = document.getElementById('techniqueInfo');
const paramsPanel = document.getElementById('paramsPanel');
const paramsContent = document.getElementById('paramsContent');
const inputText = document.getElementById('inputText');
const outputText = document.getElementById('outputText');
const outputContainer = document.getElementById('outputContainer');
const loadingSpinner = document.getElementById('loadingSpinner');
const extraInfo = document.getElementById('extraInfo');
const executeBtn = document.getElementById('executeBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');

// Load techniques on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTechniques();
    setupEventListeners();
});

async function loadTechniques() {
    try {
        const response = await fetch('/api/techniques');
        const data = await response.json();
        
        techniqueSelect.innerHTML = '<option value="">-- Select a Technique --</option>';
        data.techniques.forEach(technique => {
            const option = document.createElement('option');
            option.value = technique;
            option.textContent = technique;
            techniqueSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading techniques:', error);
        techniqueSelect.innerHTML = '<option value="">Error loading techniques</option>';
    }
}

function setupEventListeners() {
    // Technique selection
    techniqueSelect.addEventListener('change', (e) => {
        currentTechnique = e.target.value;
        updateTechniqueInfo();
        updateParamsPanel();
    });
    
    // Operation tabs
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', (e) => {
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            e.currentTarget.classList.add('active');
            currentOperation = e.currentTarget.dataset.operation;
            updateInputPlaceholder();
        });
    });
    
    // Execute button
    executeBtn.addEventListener('click', executeOperation);
    
    // Clear button
    clearBtn.addEventListener('click', () => {
        inputText.value = '';
        outputText.innerHTML = 'Results will appear here...';
        outputText.className = 'output-text';
        extraInfo.classList.remove('show');
        extraInfo.innerHTML = '';
        copyBtn.style.display = 'none';
    });
    
    // Copy button
    copyBtn.addEventListener('click', () => {
        const textToCopy = outputText.textContent;
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<span class="icon">✓</span> Copied!';
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
            }, 2000);
        });
    });
    
    // Enter key to execute
    inputText.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            executeOperation();
        }
    });
}

function updateTechniqueInfo() {
    if (!currentTechnique) {
        techniqueInfo.classList.remove('show');
        return;
    }
    
    const descriptions = {
        'CaesarCipher': 'Classical substitution cipher that shifts letters by a fixed offset. Simple but historically significant.',
        'AESCipher': 'Advanced Encryption Standard - industry-standard symmetric encryption with 128/192/256-bit keys.',
    };
    
    techniqueInfo.innerHTML = descriptions[currentTechnique] || 'Modern encryption technique.';
    techniqueInfo.classList.add('show');
}

function updateParamsPanel() {
    if (!currentTechnique) {
        paramsPanel.style.display = 'none';
        return;
    }
    
    if (currentTechnique === 'CaesarCipher') {
        paramsContent.innerHTML = `
            <div class="param-group">
                <label for="caesarOffset">Offset (1-25, optional - will prompt if not provided):</label>
                <input type="number" id="caesarOffset" class="param-input" min="1" max="25" placeholder="Leave empty for interactive prompt">
            </div>
        `;
        paramsPanel.style.display = 'block';
    } else if (currentTechnique === 'AESCipher') {
        paramsContent.innerHTML = `
            <div class="param-group">
                <label>Key Size:</label>
                <div class="param-radio-group">
                    <label>
                        <input type="radio" name="keySize" value="128" checked>
                        128-bit
                    </label>
                    <label>
                        <input type="radio" name="keySize" value="192">
                        192-bit
                    </label>
                    <label>
                        <input type="radio" name="keySize" value="256">
                        256-bit
                    </label>
                </div>
            </div>
            <div class="param-group">
                <label for="customKey">Custom Key (optional - leave empty for random):</label>
                <input type="text" id="customKey" class="param-input" placeholder="Leave empty for random key generation">
            </div>
        `;
        paramsPanel.style.display = 'block';
    } else {
        paramsPanel.style.display = 'none';
    }
}

function updateInputPlaceholder() {
    const placeholders = {
        'E': 'Enter plaintext to encrypt...',
        'D': 'Enter ciphertext to decrypt...',
        'B': 'Enter ciphertext to brute force...'
    };
    inputText.placeholder = placeholders[currentOperation] || 'Enter text here...';
}

async function executeOperation() {
    if (!currentTechnique) {
        showError('Please select a technique first');
        return;
    }
    
    const text = inputText.value.trim();
    if (!text) {
        showError('Please enter some text');
        return;
    }
    
    // Gather parameters
    const params = {};
    
    if (currentTechnique === 'CaesarCipher') {
        const offsetInput = document.getElementById('caesarOffset');
        if (offsetInput && offsetInput.value) {
            params.offset = parseInt(offsetInput.value);
        }
    } else if (currentTechnique === 'AESCipher') {
        const selectedKeySize = document.querySelector('input[name="keySize"]:checked');
        if (selectedKeySize) {
            params.key_size = parseInt(selectedKeySize.value);
        }
        const customKeyInput = document.getElementById('customKey');
        if (customKeyInput && customKeyInput.value.trim()) {
            params.custom_key = customKeyInput.value.trim();
        }
    }
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                technique: currentTechnique,
                operation: currentOperation,
                input_text: text,
                params: params
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showError(data.error || 'An error occurred');
            return;
        }
        
        showResult(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to server');
    }
}

function showLoading() {
    outputText.style.display = 'none';
    loadingSpinner.style.display = 'flex';
    extraInfo.classList.remove('show');
    copyBtn.style.display = 'none';
}

function showResult(data) {
    loadingSpinner.style.display = 'none';
    outputText.style.display = 'block';
    
    if (data.success) {
        outputText.className = 'output-text success';
        
        // Handle different result types
        if (Array.isArray(data.result)) {
            // Brute force results
            let html = '<div class="brute-force-results">';
            data.result.forEach((item, index) => {
                html += `<div class="brute-force-item" onclick="selectBruteForceResult(this)">
                    <strong>Option ${index + 1}:</strong> ${escapeHtml(item)}
                </div>`;
            });
            html += '</div>';
            outputText.innerHTML = html;
        } else {
            outputText.textContent = data.result;
        }
        
        // Show extra info for AES
        if (data.extra_info && Object.keys(data.extra_info).length > 0) {
            let infoHtml = '';
            if (data.extra_info.key_hex) {
                infoHtml += `<strong>Key (Hex):</strong> ${data.extra_info.key_hex}<br>`;
            }
            if (data.extra_info.key_size) {
                infoHtml += `<strong>Key Size:</strong> ${data.extra_info.key_size}-bit<br>`;
            }
            if (data.extra_info.num_rounds) {
                infoHtml += `<strong>Rounds:</strong> ${data.extra_info.num_rounds}`;
            }
            extraInfo.innerHTML = infoHtml;
            extraInfo.classList.add('show');
        }
        
        copyBtn.style.display = 'block';
    } else {
        showError(data.error || 'Unknown error');
    }
}

function showError(message) {
    loadingSpinner.style.display = 'none';
    outputText.style.display = 'block';
    outputText.className = 'output-text error';
    outputText.textContent = '❌ ' + message;
    extraInfo.classList.remove('show');
    copyBtn.style.display = 'none';
}

function selectBruteForceResult(element) {
    // Remove previous selection
    document.querySelectorAll('.brute-force-item').forEach(item => {
        item.style.background = 'rgba(15, 23, 42, 0.8)';
    });
    // Highlight selected
    element.style.background = 'rgba(99, 102, 241, 0.3)';
    
    // Copy to clipboard
    const text = element.textContent.replace(/^Option \d+: /, '');
    navigator.clipboard.writeText(text);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
