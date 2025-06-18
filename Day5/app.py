import streamlit as st
from PyPDF2 import PdfReader
from utils import Utils
import json
# Replace these with your LangChain functions
# from summarizer import summarize_text
# from question_generator import generate_mcqs

st.set_page_config(page_title="🧠 Study Assistant", layout="centered")
st.title("📚 Study Assistant: Summarizer + Quiz Generator")

uploaded_file = st.file_uploader("Upload your PDF study material", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    if text.strip():
        with st.spinner("🧠 Summarizing content..."):
            util = Utils()
            summary = util.summarise(text)
            st.subheader("🔍 Summary")
            st.write(summary)

        with st.spinner("📝 Generating quiz questions..."):
            mcq_res_json = util.generate_mcqs(summary)
            print("questions = ", mcq_res_json)

        st.subheader("📝 Take the Quiz")

        mcqs = json.loads(mcq_res_json)
        print("mcqs_json = ", mcq_res_json)
        user_answers = []
        for idx, mcq in enumerate(mcqs):
            st.markdown(f"**Q{idx + 1}. {mcq['question']}**")

            options = mcq['options']
            option_map = {}
            for opt in options:
                if ")" in opt:
                    key, val = opt.split(")", 1)
                    option_map[key.strip()] = val.strip()

            answer = st.radio(
                label="Choose an option:",
                options=list(option_map.keys()),
                format_func=lambda k: option_map[k],
                key=f"mcq_{idx}"
            )

            st.markdown(f"**Correct Answer:** {mcq['answer']}")

    # st.write(mcq_res_json)
