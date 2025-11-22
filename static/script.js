// Global state
let currentTechnique = "";
let currentOperation = "E";

// DOM Elements
const techniqueSelect = document.getElementById("techniqueSelect");
const techniqueInfo = document.getElementById("techniqueInfo");
const paramsPanel = document.getElementById("paramsPanel");
const paramsContent = document.getElementById("paramsContent");
const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");
const outputContainer = document.getElementById("outputContainer");
const loadingSpinner = document.getElementById("loadingSpinner");
const extraInfo = document.getElementById("extraInfo");
const executeBtn = document.getElementById("executeBtn");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");

// Load techniques on page load
document.addEventListener("DOMContentLoaded", () => {
  loadTechniques();
  setupEventListeners();
});

async function loadTechniques() {
  try {
    const response = await fetch("/api/techniques");
    const data = await response.json();

    techniqueSelect.innerHTML =
      '<option value="">-- Select a Technique --</option>';
    data.techniques.forEach((technique) => {
      const option = document.createElement("option");
      option.value = technique;
      option.textContent = technique;
      techniqueSelect.appendChild(option);
    });
  } catch (error) {
    console.error("Error loading techniques:", error);
    techniqueSelect.innerHTML =
      '<option value="">Error loading techniques</option>';
  }
}

function setupEventListeners() {
  // Technique selection
  techniqueSelect.addEventListener("change", (e) => {
    currentTechnique = e.target.value;
    updateTechniqueInfo();
    updateParamsPanel();
  });

  // Operation tabs
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.addEventListener("click", (e) => {
      document
        .querySelectorAll(".tab-button")
        .forEach((btn) => btn.classList.remove("active"));
      e.currentTarget.classList.add("active");
      currentOperation = e.currentTarget.dataset.operation;
      updateInputPlaceholder();
    });
  });

  // Execute button
  executeBtn.addEventListener("click", executeOperation);

  // Clear button
  clearBtn.addEventListener("click", () => {
    inputText.value = "";
    outputText.innerHTML = "Results will appear here...";
    outputText.className = "output-text";
    extraInfo.classList.remove("show");
    extraInfo.innerHTML = "";
    copyBtn.style.display = "none";
  });

  // Copy button
  copyBtn.addEventListener("click", () => {
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
  inputText.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.key === "Enter") {
      executeOperation();
    }
  });
}

function updateTechniqueInfo() {
    if (!currentTechnique) {
        techniqueInfo.classList.remove('show');
        return;
    }
    
    // Fetch technique info from API
    fetch(`/api/technique_info/${currentTechnique}`)
        .then(response => response.json())
        .then(data => {
            if (data.description) {
                techniqueInfo.innerHTML = data.description;
                techniqueInfo.classList.add('show');
            }
        })
        .catch(error => {
            console.error('Error fetching technique info:', error);
            techniqueInfo.innerHTML = 'Modern encryption technique.';
            techniqueInfo.classList.add('show');
        });
}

function updateParamsPanel() {
    if (!currentTechnique) {
        paramsPanel.style.display = 'none';
        return;
    }
    
    // Fetch technique parameters from API
    fetch(`/api/technique_info/${currentTechnique}`)
        .then(response => response.json())
        .then(data => {
            if (data.params && data.params.length > 0) {
                paramsContent.innerHTML = generateParamsHTML(data.params);
                paramsPanel.style.display = 'block';
            } else {
                paramsPanel.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching technique parameters:', error);
            paramsPanel.style.display = 'none';
        });
}

function generateParamsHTML(params) {
    let html = '';
    
    params.forEach(param => {
        html += '<div class="param-group">';
        html += `<label>${param.label || param.name}</label>`;
        
        if (param.type === 'radio' && param.options) {
            html += '<div class="param-radio-group">';
            param.options.forEach(option => {
                const isDefault = param.default === option.value;
                html += `<label>
                    <input type="radio" name="${param.name}" value="${option.value}" ${isDefault ? 'checked' : ''}>
                    ${option.label}
                </label>`;
            });
            html += '</div>';
        } else if (param.type === 'number') {
            html += `<input type="number" id="${param.name}" class="param-input" 
                placeholder="${param.placeholder || ''}"
                ${param.min !== undefined ? `min="${param.min}"` : ''}
                ${param.max !== undefined ? `max="${param.max}"` : ''}
                ${param.required ? 'required' : ''}>`;
        } else {
            // Default to text input
            html += `<input type="text" id="${param.name}" class="param-input"
                placeholder="${param.placeholder || ''}"
                ${param.required ? 'required' : ''}>`;
        }
        
        html += '</div>';
    });
    
    return html;
}

function updateInputPlaceholder() {
  const placeholders = {
    E: "Enter plaintext to encrypt...",
    D: "Enter ciphertext to decrypt...",
    B: "Enter ciphertext to brute force...",
  };
  inputText.placeholder =
    placeholders[currentOperation] || "Enter text here...";
}

async function executeOperation() {
  if (!currentTechnique) {
    showError("Please select a technique first");
    return;
  }

  const text = inputText.value.trim();
  if (!text) {
    showError("Please enter some text");
    return;
  }

  // Gather parameters dynamically from the params panel
  const params = {};
  
  // Get all input fields in the params panel
  const inputs = paramsContent.querySelectorAll('input, select');
  inputs.forEach(input => {
    if (input.type === 'radio') {
      if (input.checked) {
        params[input.name] = isNaN(input.value) ? input.value : parseInt(input.value);
      }
    } else if (input.type === 'number') {
      if (input.value) {
        params[input.id] = parseInt(input.value);
      }
    } else if (input.type === 'text') {
      if (input.value.trim()) {
        params[input.id] = input.value.trim();
      }
    }
  });


  // Show loading
  showLoading();

  try {
    const response = await fetch("/api/execute", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        technique: currentTechnique,
        operation: currentOperation,
        input_text: text,
        params: params,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "An error occurred");
      return;
    }

    showResult(data);
  } catch (error) {
    console.error("Error:", error);
    showError("Failed to connect to server");
  }
}

function showLoading() {
  outputText.style.display = "none";
  loadingSpinner.style.display = "flex";
  extraInfo.classList.remove("show");
  copyBtn.style.display = "none";
}

function showResult(data) {
  loadingSpinner.style.display = "none";
  outputText.style.display = "block";

  if (data.success) {
    outputText.className = "output-text success";

    // Handle different result types
    if (Array.isArray(data.result)) {
      // Brute force results
      let html = '<div class="brute-force-results">';
      data.result.forEach((item, index) => {
        html += `<div class="brute-force-item" onclick="selectBruteForceResult(this)">
                    <strong>Option ${index + 1}:</strong> ${escapeHtml(item)}
                </div>`;
      });
      html += "</div>";
      outputText.innerHTML = html;
    } else {
      outputText.textContent = data.result;
    }

    // Show extra info if available
    if (data.extra_info && Object.keys(data.extra_info).length > 0) {
      let infoHtml = "";

      // Show key information prominently
      if (data.extra_info.key_hex) {
        infoHtml += `<div style="margin-bottom: 1rem; padding: 1rem; background: rgba(99, 102, 241, 0.15); border-left: 4px solid var(--primary-color); border-radius: 8px;">`;
        infoHtml += `<strong style="color: var(--primary-light); font-size: 1.1rem;">🔑 Encryption Key:</strong><br>`;
        infoHtml += `<div style="margin-top: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">`;
        infoHtml += `<code style="flex: 1; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; font-family: 'Consolas', monospace; word-break: break-all; color: var(--text-primary);">${data.extra_info.key_hex}</code>`;
        infoHtml += `<button onclick="copyKey('${data.extra_info.key_hex}')" style="padding: 0.5rem 1rem; background: var(--primary-color); border: none; border-radius: 6px; color: white; cursor: pointer; white-space: nowrap; font-weight: 600;">📋 Copy</button>`;
        infoHtml += `</div>`;

        // Show UTF-8 representation if available
        if (data.extra_info.key_utf8) {
          infoHtml += `<div style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-secondary);">`;
          infoHtml += `<strong>UTF-8:</strong> <code style="background: rgba(0,0,0,0.2); padding: 0.25rem 0.5rem; border-radius: 4px;">${escapeHtml(
            data.extra_info.key_utf8
          )}</code>`;
          infoHtml += `</div>`;
        }

        infoHtml += `<div style="margin-top: 0.75rem; font-size: 0.875rem; color: var(--accent-color);">`;
        infoHtml += `⚠️ <strong>Important:</strong> Save this key to decrypt your message later!`;
        infoHtml += `</div>`;
        infoHtml += `</div>`;
      }

      // Show other technique-specific info
      if (data.extra_info.key_size || data.extra_info.num_rounds) {
        infoHtml += `<div style="display: flex; gap: 1rem; flex-wrap: wrap;">`;
        if (data.extra_info.key_size) {
          infoHtml += `<div><strong>Key Size:</strong> ${data.extra_info.key_size}-bit</div>`;
        }
        if (data.extra_info.num_rounds) {
          infoHtml += `<div><strong>Rounds:</strong> ${data.extra_info.num_rounds}</div>`;
        }
        infoHtml += `</div>`;
      }

      extraInfo.innerHTML = infoHtml;
      extraInfo.classList.add("show");
    }

    copyBtn.style.display = "block";
  } else {
    showError(data.error || "Unknown error");
  }
}

function showError(message) {
  loadingSpinner.style.display = "none";
  outputText.style.display = "block";
  outputText.className = "output-text error";
  outputText.textContent = "❌ " + message;
  extraInfo.classList.remove("show");
  copyBtn.style.display = "none";
}

function selectBruteForceResult(element) {
  // Remove previous selection
  document.querySelectorAll(".brute-force-item").forEach((item) => {
    item.style.background = "rgba(15, 23, 42, 0.8)";
  });
  // Highlight selected
  element.style.background = "rgba(99, 102, 241, 0.3)";

  // Copy to clipboard
  const text = element.textContent.replace(/^Option \d+: /, "");
  navigator.clipboard.writeText(text);
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Copy key to clipboard with visual feedback
function copyKey(key) {
    navigator.clipboard.writeText(key).then(() => {
        // Find the button and update it temporarily
        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '✓ Copied!';
        button.style.background = 'var(--success-color)';
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = 'var(--primary-color)';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy key:', err);
        alert('Failed to copy key to clipboard');
    });
}
