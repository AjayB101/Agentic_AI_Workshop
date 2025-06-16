import streamlit as st
import fitz  # PyMuPDF
from agent import evaluate_student

st.set_page_config(page_title="Placement Readiness Scorer", layout="centered")
st.title("🎓 Placement Readiness Scorer")

# PDF Resume Upload
st.subheader("📄 Upload Resume (PDF)")
resume_file = st.file_uploader("Upload student resume", type=["pdf"])

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    return ""

with st.form("student_form"):
    st.subheader("📊 Academic Metrics")
    attendance = st.slider("Attendance (%)", 0, 100, 85)
    assignment_score = st.slider("Assignment Score (%)", 0, 100, 80)
    test_score = st.slider("Test Score (%)", 0, 100, 75)

    st.subheader("🗣️ Soft Skills Metrics")
    mock_interview_score = st.slider("Mock Interview Score (%)", 0, 100, 65)
    bio_quality_score = st.slider("Bio Quality Score (%)", 0, 100, 70)
    faculty_feedback_score = st.slider("Faculty Feedback Score (%)", 0, 100, 60)

    submitted = st.form_submit_button("Evaluate Readiness")

    if submitted:
        resume_text = extract_text_from_pdf(resume_file)

        student_data = {
            "attendance": attendance,
            "assignment_score": assignment_score,
            "test_score": test_score,
            "mock_interview_score": mock_interview_score,
            "bio_quality_score": bio_quality_score,
            "faculty_feedback_score": faculty_feedback_score,
            "resume_text": resume_text
        }

        with st.spinner("Evaluating..."):
            result = evaluate_student(student_data)

        st.success("Evaluation Complete ✅")
        st.markdown(f"### 📊 Result:\n{result}")
