import streamlit as st
import pandas as pd
from llms.llm_setup import get_gemini, get_phi
from agents.academic_agent import analyze_academics
from agents.softskill_agent import analyze_softskills
from agents.scorer_agent import generate_score
from agents.recommender_agent import recommend

st.set_page_config(page_title="📊 Placement Readiness Scorer", layout="centered")
st.title("🎓 Placement Readiness Evaluator")

st.subheader("📁 Upload Student Academic & Soft Skills CSV")
csv_file = st.file_uploader("Upload student data", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)
    st.dataframe(df.head())

    st.subheader("🚀 Evaluation Results")
    gemini = get_gemini()
    phi = get_phi()

    for idx, student in df.iterrows():
        academic_eval = analyze_academics(student, phi)
        softskill_eval = analyze_softskills(student, gemini)
        readiness_score = generate_score(academic_eval, softskill_eval)
        suggestion = recommend(readiness_score)

        with st.expander(f"👤 {student['name']}"):
            st.write("📘 Academic Score:", academic_eval)
            st.write("🗣️ Soft Skill Score:", softskill_eval)
            st.write("✅ Readiness Score:", readiness_score)
            st.write("🛠️ Recommended Interventions:", suggestion)
