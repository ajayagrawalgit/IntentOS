/* 
 * IntentOS Frontend Logic
 * Fast, Typed, and Dynamic
 */

document.addEventListener('DOMContentLoaded', () => {
    // 🛡️ DOM Elements
    const processBtn = document.getElementById('processBtn');
    const userInput = document.getElementById('userInput');
    const results = document.getElementById('results');
    const loader = document.getElementById('loader');
    const btnText = document.getElementById('btnText');
    const analysisContent = document.getElementById('analysisContent');
    const actionsContent = document.getElementById('actionsContent');
    const jsonContent = document.getElementById('jsonContent');

    // 🗺️ API Gateway Configuration
    // Served from the same FastAPI origin (unified deployment)
    const API_URL = '/process';

    const renderUI = (data) => {
        const { intent_analysis, executed_actions } = data;
        const severity = (intent_analysis.severity || 'low').toLowerCase();

        // 1. Render Analysis Card
        analysisContent.innerHTML = `
            <div style="margin-bottom: 0.5rem; display:flex; align-items:center; gap: 0.75rem;">
                <span class="severity-pill ${severity}">${severity}</span>
                <h4 style="font-family:var(--font-heading); color:white; font-size:1.4rem;">${intent_analysis.intent}</h4>
            </div>
            <p style="color:var(--text-muted); line-height:1.6; padding-top: 10px;">
                <strong>Identified Condition:</strong> ${intent_analysis.condition}
            </p>
        `;

        // 2. Render Actions Card
        actionsContent.innerHTML = executed_actions.map(action => {
            const isMedical = action.includes('🚑');
            const icon = isMedical ? '' : '⚡';
            return `
                <div class="action-row">
                    <span class="action-icon">${isMedical ? '' : icon}</span>
                    <span style="font-size: 0.95rem; color: #fff;">${action}</span>
                </div>
            `;
        }).join('');

        // 3. Render Raw Intelligence Card
        jsonContent.textContent = JSON.stringify(data, null, 4);

        // Transition Animation
        results.classList.add('visible');
    };

    const setLoading = (isLoading) => {
        processBtn.disabled = isLoading;
        loader.style.display = isLoading ? 'inline-block' : 'none';
        btnText.textContent = isLoading ? 'Analyzing...' : 'Process Intent';
        const sendIcon = document.querySelector('.send-icon');
        if (sendIcon) sendIcon.style.display = isLoading ? 'none' : 'block';
        if (isLoading) results.classList.remove('visible');
    };

    // 🚀 Primary Execution Flow
    processBtn.addEventListener('click', async () => {
        const text = userInput.value.trim();
        if (!text) return alert("Please specify an intent to analyze.");

        setLoading(true);

        try {
            console.log(`Sending to ${API_URL}: ${text}`);
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                throw new Error(`Cloud failure: ${response.status}`);
            }

            const data = await response.json();
            renderUI(data);

        } catch (error) {
            console.error("Transmission Error:", error);
            analysisContent.innerHTML = `
                <div class="severity-pill high">Critical Error</div>
                <p style="color:#f87171; margin-top:1rem;">Failed to connect to IntentOS Gateway. Ensure backend is active.</p>
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
