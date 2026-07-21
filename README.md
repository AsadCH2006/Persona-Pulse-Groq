# 🤖 PersonaPulse - Groq AI Assistant

PersonaPulse is a real-time, high-performance AI chatbot web application built with **Streamlit** and powered by **Groq LLAMA models**. It features dynamic system persona enforcement, real-time response streaming, and interactive theme customization.

---

## ✨ Key Features

* ⚡ **Ultra-Fast Streaming Responses:** Powered by Groq LPU™ Inference Engine for instantaneous response generation.
* 🎭 **Dynamic System Personas:**
  * ✈️ **Travel Guide Mode:** Specializes in travel itineraries, local cultures, destination planning, and packing advice.
  * 💻 **Tech Support Specialist Mode:** Handles hardware troubleshooting, software diagnostics, operating systems, and networking.
  * 🔒 **Strict Role Enforcement:** Rejects out-of-scope prompts politely based on the active role.
* 🎨 **Dynamic Dynamic UI & Theme Switching:** Custom 3-color palette adaptation and layout adjustments matching the active persona.
* ⚙️ **Flexible Model Selection:** Toggle between high-capability (`llama-3.3-70b-versatile`) and high-speed (`llama-3.1-8b-instant`) models.
* 🔑 **Secure Key Management:** Input keys via the sidebar or deploy seamlessly using Streamlit Secrets (`secrets.toml`).

---

## 🛠️ Project Structure

```text
Persona-Pulse-Groq/
│
├── app.py             # Main Streamlit application and UI layout
├── requirements.txt   # Project dependencies (streamlit, groq)
├── .gitignore         # Ignores sensitive environment keys and temporary files
└── README.md          # Project documentation
```

---

## 🚀 Quickstart & Local Installation

### Prerequisites

* Python 3.9 or higher
* A free Groq API Key from [Groq Console](https://console.groq.com)

### 1. Clone the Repository
```bash
git clone https://github.com/AsadCH2006/Persona-Pulse-Groq.git
cd Persona-Pulse-Groq
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets (Optional)
Create a `.streamlit/secrets.toml` file in the root directory:
```toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"
```

### 4. Run the Streamlit Application
```bash
python -m streamlit run app.py
```

---

## ☁️ Deployment

This repository is optimized for deployment on **Streamlit Community Cloud**:
1. Fork or push this repository to GitHub.
2. Connect your repository to [share.streamlit.io](https://share.streamlit.io).
3. Add `GROQ_API_KEY` under **Advanced Settings -> Secrets**.
4. Deploy!

---

## 💻 Tech Stack

* **Frontend / Framework:** [Streamlit](https://streamlit.io/)
* **AI Model Engine:** [Groq Cloud API](https://groq.com/)
* **Language:** Python 3.10+
