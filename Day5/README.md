# 📚 Study Assistant: Summarizer + Quiz Generator

A Streamlit web app that lets you:

- Upload a study material PDF
- Summarize its content using LLM
- Generate a short quiz (MCQs) from the summary
- Take the quiz interactively

---

## 🚀 Features

- PDF Text Extraction (via `PyPDF2`)
- Summarization using an LLM (LangChain compatible)
- Quiz Generation (MCQs) using LLM with structured output
- Interactive Quiz UI with score capture (optional)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Day5
```

### 2. Create Virtual Environment

**Option A: Using Conda**

```bash
conda create -n study-assistant python=3.10
conda activate study-assistant
```

**Option B: Using venv**

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables

Create a `.env` file in the project root and add your Groq API key:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

---

## 📋 Requirements

Make sure your `requirements.txt` includes:

```
streamlit
PyPDF2
langchain
langchain-groq
python-dotenv
```

---

## 🎯 Usage

1. Start the application using `streamlit run app.py`
2. Upload a PDF file containing your study material
3. Click "Summarize" to generate a summary
4. Click "Generate Quiz" to create MCQs from the summary
5. Take the interactive quiz and see your results

---

## 🔧 Troubleshooting

- Ensure you have a valid Groq API key in your `.env` file
- Make sure all dependencies are installed correctly
- Check that your PDF files are readable and not corrupted
- Verify your Python version is 3.10 or compatible
