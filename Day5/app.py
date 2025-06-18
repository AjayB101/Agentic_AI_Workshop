import streamlit as st
from PyPDF2 import PdfReader
from utils import Utils
# Replace these with your LangChain functions
# from summarizer import summarize_text
# from question_generator import generate_mcqs

st.set_page_config(page_title="🧠 Study Assistant", layout="centered")
st.title("📚 Study Assistant: Summarizer + Quiz Generator")

uploaded_file = st.file_uploader("Upload your PDF study material", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text=""
    for page in reader.pages:
        text+=page.extract_text()
        

    st.subheader("📄 Extracted Text")
    with st.expander("Click to view raw extracted content"):
        st.write(text)

    if text.strip():
        with st.spinner("🧠 Summarizing content..."):
            util=Utils()
            summary = util.summarise(text)
            st.write(summary)
        st.subheader("🔍 Summary")
        st.markdown("\n".join(f"• {line}" for line in summary.split("\n")))

        with st.spinner("📝 Generating quiz questions..."):
            mcq_res_json =  util.generate_mcqs(summary)
            print("questions = ",mcq_res_json)

        st.subheader("❓ Quiz Questions")
        
        # st.write(mcq_res_json)
          
