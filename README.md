# 📝 Patient Note Rewriter (Ollama)

This Streamlit app transforms raw patient input into medical notes using a **local LLM (Ollama)**. It supports two modes of rewriting:

- 📄 **Formal HPI** — Professional, physician-style documentation  
- 🧑‍⚕️ **Patient Summary** — Natural, first-person narrative for patient portals  
- 🔁 **Comparison Mode** — Side-by-side generation of both formats  

---

## 🚀 Features

- Toggle between **Single Mode** and **Comparison Mode**
- Input raw patient speech and rewrite using local LLM
- Clean, scrollable outputs with copyable formatting
- Download outputs individually or together
- Works entirely offline with local Ollama backend

---

## 📦 Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) with a supported model (e.g., `llama3.3`)

Install required Python packages:
```bash
pip install -r requirements.txt
```
---

## 💻 How to Use

1. Clone the repository
2. Start Ollama with a local model:
```bash
ollama pull llama3
ollama run llama3
```

3. Run the app:
```bash
streamlit run app.py
```
---
## 🧠 Why This Exists

This tool was created as a lightweight, hands-on way to explore how local large language models (LLMs) can reshape patient communication into structured medical notes.
Rather than aiming for clinical deployment or publication, it's meant to serve as a practical sandbox for:

🧪 Testing how different prompt styles affect output  
🩺 Exploring the shift from patient language to clinician documentation  
🤖 Prototyping AI-powered pre-charting tools or chatbot integrations  
💼 Showcasing prompt engineering and UI design in healthcare contexts  
It’s designed to be simple, local, and easy to adapt for your own curiosity or clinical AI projects.

---
## ⚠️ Disclaimer

This tool is for demonstration and research purposes only.
It is not intended for clinical use or to replace professional medical judgment.