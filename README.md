# IntentOS | Multi-Sensory AI Emergency Orchestrator

**Production-Ready, Multi-Sensory AI Response Engine**

IntentOS is a world-class AI orchestrator designed to convert complex, multi-sensory human inputs—text, images, video, and voice—into structured, actionable intelligence. Built for mission-critical scenarios, it ensures that human intent is analyzed with precision and executed through real-world Google Cloud integrations.

---

## 🚀 Live Demo
**Link**: [https://intent-os-217442463149.us-central1.run.app](https://intent-os-217442463149.us-central1.run.app)

---

## 🧠 Core Features

### 1. Multi-Sensory Intelligence (Multimodal)
Powered by **Google Gemini 2.0 Flash**, IntentOS processes more than just text. It can "see" images and video, and "hear" voice recordings to provide a deep, contextual analysis of any emergency or request.

### 2. Verified Identity Integration
Seamlessly integrated with **Google Identity Services (GIS)**. User intents are linked to verified Google profiles, ensuring a secure and accountable chain of communication during critical incidents.

### 3. Precision Orchestration (Proportional Response)
The system executes real-world actions based on AI-assessed severity:
- **High/Medium Severity**: Automatically triggers **Google Maps Elevation API** for precise altitude data and dispatches emergency notifications via **Gmail SMTP**.
- **Low Severity**: Provides safety confirmation and simulated resolutions without over-escalating.

### 4. Voice Verification (Listen-Back)
A specialized in-browser MediaRecorder allows users to record their intent and **verify it** with an instant playback player before initiating analysis.

### 5. Premium Glassmorphic UI
A high-fidelity frontend built with Vanilla JS and Modern CSS:
- **Aesthetic**: Dark Obsidian theme with backdrop-blur and dynamic severity-based color shifting.
- **Micro-Animations**: Smooth transitions and real-time status feedback.

---

## 🛠️ Tech Stack
- **AI Engine**: Google GenAI (Gemini 2.0 Flash)
- **Backend**: Python 3.11 + FastAPI
- **Frontend**: HTML5 + Vanilla JS + Modern CSS
- **APIs**: Google Maps (Elevation), Google Identity (GIS), Gmail SMTP
- **Infrastructure**: Docker + Google Cloud Run (Serverless)

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- Google Gemini API Key (from Google AI Studio)
- Gmail App Password (for emergency alerts)

### Installation
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/intent-os.git
    cd intent-os
    ```
2.  **Environment Setup**:
    Copy `.env.template` to `.env` and fill in your credentials.
3.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```
4.  **Launch**:
    ```bash
    python3 backend/main.py
    ```

---

## ⚡ Hackathon Submission Notes
**Mission**: Creating a "Never-Fail" system for human intent.
**Technical Differentiator**: The combination of multimodal deep analysis and automated Google Service orchestration ensures that **IntentOS** provides the most reliable and actionable response to any emergency.
