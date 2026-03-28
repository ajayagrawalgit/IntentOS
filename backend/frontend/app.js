/* 
 * IntentOS v3 Frontend Logic
 * Multimodal, Location-Aware, and Identity-Integrated
 */

// 🗝️ Identity Decoder (Simple JWT Parser)
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        return JSON.parse(window.atob(base64));
    } catch (e) { return null; }
}

// 🛡️ Global State
let currentUser = null;
let currentCoords = null;
let currentFile = null;
let mediaRecorder = null;
let audioChunks = [];

// 🎓 Google Identity Callback
window.handleCredentialResponse = (response) => {
    const payload = parseJwt(response.credential);
    if (payload) {
        currentUser = {
            name: payload.name,
            email: payload.email,
            picture: payload.picture
        };
        document.querySelector('.g_id_signin').classList.add('hidden');
        const userBadge = document.getElementById('userBadge');
        document.getElementById('userName').textContent = payload.given_name || payload.name;
        document.getElementById('userImg').src = payload.picture;
        userBadge.classList.remove('hidden');
        console.log("Identity Verified:", currentUser.email);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // 🏗️ DOM Elements
    const processBtn = document.getElementById('processBtn');
    const userInput = document.getElementById('userInput');
    const intentHint = document.getElementById('intentHint');
    const results = document.getElementById('results');
    const loader = document.getElementById('loader');
    const btnText = document.getElementById('btnText');
    const analysisContent = document.getElementById('analysisContent');
    const actionsContent = document.getElementById('actionsContent');
    const jsonContent = document.getElementById('jsonContent');
    
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const micBtn = document.getElementById('micBtn');
    const mediaPreview = document.getElementById('mediaPreview');
    const locText = document.getElementById('locText');
    const locationChip = document.getElementById('locationStatus');

    // 📍 Geolocation Engine
    const initLocation = () => {
        if (!navigator.geolocation) return;
        locText.textContent = "Requesting Location...";
        
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                currentCoords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
                locText.textContent = "Location Active";
                locationChip.classList.add('active');
            },
            (err) => {
                locText.textContent = "Location Denied";
                locationChip.classList.remove('active');
                console.warn("Location Access Denied:", err.message);
            }
        );
    };
    initLocation();

    // 🎤 Audio Recording Engine
    micBtn.addEventListener('click', async () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            micBtn.classList.remove('recording');
            return;
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(audioChunks, { type: 'audio/webm' });
                const audioURL = URL.createObjectURL(blob);
                currentFile = new File([blob], "voice_input.webm", { type: 'audio/webm' });
                updateMediaPreview("🎤 Voice Recording Captured", currentFile, audioURL);
            };

            mediaRecorder.start();
            micBtn.classList.add('recording');
        } catch (err) {
            alert("Microphone access is required for voice chat.");
        }
    });

    // 📁 File Handling Engine
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            currentFile = file;
            updateMediaPreview(file.name, file);
        }
    });

    const updateMediaPreview = (name, file = null, audioURL = null) => {
        let playbackHtml = "";
        if (audioURL) {
            playbackHtml = `
                <div class="audio-verify">
                    <span style="font-size:0.8rem; color:var(--text-muted);">Verify Recording:</span>
                    <audio controls src="${audioURL}" style="height: 30px;"></audio>
                </div>
            `;
        }

        mediaPreview.innerHTML = `
            <div class="location-chip active" style="background:var(--primary); color:white; flex-direction:column; align-items:flex-start; height:auto; padding:1rem; border-radius:16px; gap:0.75rem;">
                <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
                    <span>${name}</span>
                    <span style="margin-left:8px; cursor:pointer;" id="clearMedia">✕</span>
                </div>
                ${playbackHtml}
            </div>
        `;
        document.getElementById('clearMedia').onclick = () => {
            currentFile = null;
            mediaPreview.innerHTML = "";
            fileInput.value = "";
        };
    };

    const renderUI = (data) => {
        const { intent_analysis, executed_actions } = data;
        let severity = (intent_analysis.severity || 'low').toLowerCase();
        if (severity === 'none' || !severity || severity === 'info') severity = 'low';

        // 1. Render Analysis Card with v3 Schema (Immediate vs Simulated)
        const immediateSteps = intent_analysis.immediate_actions || [];
        const condition = intent_analysis.condition || "Situation analyzed.";
        
        // ONLY show immediate actions for High/Medium
        const isCritical = severity === 'high' || severity === 'medium';
        const showImmediate = immediateSteps.length > 0 && isCritical;

        const immediatePalette = {
            high: {
                block: 'rgba(239, 68, 68, 0.12)',
                border: '#ef4444',
                title: '#f87171',
            },
            medium: {
                block: 'rgba(245, 158, 11, 0.12)',
                border: '#f59e0b',
                title: '#fbbf24',
            },
            low: {
                block: 'rgba(255, 255, 255, 0.05)',
                border: 'rgba(255, 255, 255, 0.2)',
                title: 'var(--text-muted)',
            },
        };
        const pal = immediatePalette[severity] || immediatePalette.high;

        let immediateHtml = "";
        if (showImmediate) {
            immediateHtml = `
                <div style="background: ${pal.block}; border-left: 3px solid ${pal.border}; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                    <h5 style="font-size: 0.8rem; color: ${pal.title}; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;">Immediate Life-Saving Actions</h5>
                    <ul style="color: white; font-size: 0.95rem; line-height: 1.6; padding-left: 1.2rem;">
                        ${immediateSteps.map(step => `<li>${step}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        analysisContent.innerHTML = `
            <div style="margin-bottom: 0.8rem; display:flex; align-items:center; gap: 0.75rem;">
                <span class="severity-pill ${severity}">${severity}</span>
                <h4 style="font-family:var(--font-heading); color:white; font-size:1.4rem;">${intent_analysis.intent}</h4>
            </div>
            ${immediateHtml}
            <p style="color:var(--text-muted); line-height:1.6; font-size: 0.95rem;">
                <strong>Deep Analysis:</strong> ${condition}
            </p>
        `;

        // 2. Render Orchestration Card
        const orchHeader = severity === 'low'
            ? `<div class="orchestration-banner orchestration-banner--safe">Safety confirmed — non-emergency orchestration</div>`
            : '';
        const rows = executed_actions.map(action => {
            let icon = '⚡';
            if (action.includes('✅')) icon = '✅';
            if (action.includes('📧')) icon = '📧';
            if (action.includes('📍')) icon = '📍';
            if (action.includes('🤖')) icon = '🤖';
            if (action.includes('🚨')) icon = '🚨';

            return `
                <div class="action-row">
                    <span class="action-icon">${icon}</span>
                    <span style="font-size: 0.95rem; color: #fff;">${action}</span>
                </div>
            `;
        }).join('');
        actionsContent.innerHTML = orchHeader + rows;

        // 3. Render Raw Intelligence Card
        jsonContent.textContent = JSON.stringify(data, null, 4);
        results.classList.add('visible');
    };

    const setLoading = (isLoading) => {
        processBtn.disabled = isLoading;
        loader.style.display = isLoading ? 'inline-block' : 'none';
        btnText.textContent = isLoading ? 'Analyzing Inputs...' : 'Analyze & Get Help';
        const sendIcon = document.querySelector('.send-icon');
        if (sendIcon) sendIcon.style.display = isLoading ? 'none' : 'block';
        if (isLoading) results.classList.remove('visible');
    };

    // 🚀 Primary Execution Flow
    processBtn.addEventListener('click', async () => {
        const text = userInput.value.trim();
        const hint = intentHint.value;

        // Force Login check for medical/emergency
        if ((hint === 'medical' || text.toLowerCase().includes('emergency')) && !currentUser) {
            return alert("Google Sign-in is required for emergency intent validation.");
        }

        // Force Location check for medical
        if (hint === 'medical' && !currentCoords) {
            return alert("Real-time location sharing is required for medical emergencies. Please enable GPS.");
        }

        if (!text && !currentFile) {
            return alert("Please provide text, image, or voice input.");
        }

        setLoading(true);

        try {
            // Build Multipart Form Data
            const formData = new FormData();
            formData.append('text', text);
            formData.append('intent_hint', hint);
            
            if (currentCoords) {
                formData.append('lat', currentCoords.lat);
                formData.append('lng', currentCoords.lng);
            }
            
            if (currentUser) {
                formData.append('user_details', JSON.stringify(currentUser));
            }
            
            if (currentFile) {
                formData.append('file', currentFile);
            }

            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error("Processing failure.");

            const data = await response.json();
            renderUI(data);

        } catch (error) {
            console.error("Transmission Error:", error);
            analysisContent.innerHTML = `
                <div class="severity-pill high">System Disruption</div>
                <p style="color:#f87171; margin-top:1rem;">Orchestration Gateway unreachable. Ensure backend is healthy.</p>
            `;
            results.classList.add('visible');
        } finally {
            setLoading(false);
        }
    });

    // 🧩 Keyboard Shortcuts
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
            processBtn.click();
        }
    });
});
