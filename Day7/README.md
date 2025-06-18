# Agentic_AI_Workshop

# 🎓 Placement Readiness Scorer

An interactive Streamlit app to evaluate student placement readiness using academic scores, soft skills, and AI-powered feedback. It enables uploading a CSV file and asking natural-language questions like:

- _“Show students below 70%”_
- _“How can Avni improve?”_
- _“Who needs communication training?”_

---

## 🔧 Features

- 📊 Calculates academic & communication scores
- 🧠 Uses Gemini (Google) and Phi-3 (HuggingFace) LLMs
- 💬 Accepts natural language prompts to filter students
- 📝 Generates improvement suggestions
- 📥 Accepts resume uploads for future RAG-based extensions

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
cd placement-readiness-scorer
pip install -r requirements.txt
```

add your 
hugging face and gemini token in models_utils.py

Run the app
streamlit run app.py

upload the csv sample_data_100_students 

✨ Example Prompts
You can type queries like:

"Show students below 60%"

"How can Neha Sharma improve?"

"Who are the top performers?"

"Students with communication issues"

"Show all students"

The AI will respond accordingly with insights and suggestions.