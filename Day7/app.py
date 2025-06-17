import streamlit as st
import pandas as pd
from scoring import (
    AcademicPerformanceAgent,
    SoftSkillInsightAgent,
    ReadinessScoringAgent,
    InterventionRecommenderAgent,
)
from rag_utils import extract_text_from_file
from model_utils import get_gemini_llm

st.set_page_config(
    page_title="📊 Placement Readiness Scorer", layout="centered")
st.title("🎓 Placement Readiness Scorer")

st.subheader("📥 Upload Student CSV")
csv_file = st.file_uploader("Upload CSV", type="csv")

st.subheader("💬 Enter LinkedIn Bio")
linkedin_bio = st.text_area("Paste LinkedIn Bio")

st.subheader("📄 Upload Resume (PDF/DOCX/TXT)")
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

if st.button("🚀 Generate Scores") and csv_file:
    df = pd.read_csv(csv_file)
    llm = get_gemini_llm()

    if resume_file:
        resume_text = extract_text_from_file(resume_file)
    else:
        resume_text = ""

    for idx, row in df.iterrows():
        st.markdown(f"---\n### 👤 {row['name']}")

        academic_score, reason = AcademicPerformanceAgent(row)
        st.write(f"**Academic Score:** {academic_score:.2f}%")
        st.caption(reason)

        with st.spinner("Analyzing communication..."):
            comm_response = SoftSkillInsightAgent(
                linkedin_bio, resume_text, llm)
        if comm_response:
            digits = "".join(filter(str.isdigit, comm_response))[:3]
            comm_score = int(digits) if digits else 50
        else:
            comm_score = 50

        st.write(f"**Communication Score:** {comm_score}%")
        st.caption(comm_response)

        overall, tech, comm = ReadinessScoringAgent(academic_score, comm_score)
        st.success(f"**🏁 Final Readiness Score:** {overall}%")
        st.write(f"- Tech Readiness: {tech}%")
        st.write(f"- Communication Readiness: {comm}%")

        recs = InterventionRecommenderAgent(overall, tech, comm)
        st.subheader("🔧 Recommendations")
        for rec in recs:
            st.markdown(f"- {rec}")
