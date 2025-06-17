import streamlit as st
import pandas as pd
from scoring import (
    AcademicPerformanceAgent,
    ReadinessScoringAgent,
    InterventionRecommenderAgent,
)
from rag_utils import ask_question_over_text, analyze_prompt_for_filtering
from model_utils import get_gemini_llm

st.set_page_config(
    page_title="🎯 Placement Readiness Scorer", layout="centered")
st.title("🎓 Placement Readiness Scorer")

st.subheader("📊 Upload Student CSV with Soft Skills")
csv_file = st.file_uploader("Upload CSV", type="csv")

user_prompt = st.text_input(
    "💭 Write your prompt (e.g. 'Show students below 70%', 'How can Avni improve?')")


def calculate_all_scores(df):
    """Calculate scores for all students and return structured data"""
    all_student_data = []

    for idx, row in df.iterrows():
        academic_score, reason = AcademicPerformanceAgent(row)
        comm_score = int(row.get("softskill_score", 50))
        overall, tech, comm = ReadinessScoringAgent(academic_score, comm_score)
        recs = InterventionRecommenderAgent(overall, tech, comm)

        student_data = {
            'name': row['name'],
            'academic_score': academic_score,
            'communication_score': comm_score,
            'overall_score': overall,
            'tech_readiness': tech,
            'comm_readiness': comm,
            'recommendations': recs,
            'raw_data': row
        }
        all_student_data.append(student_data)

    return all_student_data


def display_student(student_data):
    """Display a single student's information"""
    st.markdown(f"---\n### 👤 {student_data['name']}")

    st.write(f"**Academic Score:** {student_data['academic_score']:.2f}%")
    st.caption("Score from attendance, tests, assignments, and events.")

    st.write(
        f"**Communication Score:** {student_data['communication_score']}%")

    st.success(
        f"**🏁 Final Readiness Score:** {student_data['overall_score']}%")
    st.write(f"- Tech Readiness: {student_data['tech_readiness']}%")
    st.write(f"- Communication Readiness: {student_data['comm_readiness']}%")

    st.subheader("🔧 Recommendations")
    for rec in student_data['recommendations']:
        st.markdown(f"- {rec}")


if st.button("🚀 Generate") and csv_file:
    df = pd.read_csv(csv_file)
    llm = get_gemini_llm()

    # Calculate scores for all students
    all_student_data = calculate_all_scores(df)

    # If user has a specific prompt, let AI decide what to show
    if user_prompt:
        with st.spinner("🤔 Analyzing your request..."):
            # Let AI analyze the prompt and decide which students to show
            students_to_show = analyze_prompt_for_filtering(
                llm, all_student_data, user_prompt)

            if students_to_show:
                st.info(
                    f"Showing {len(students_to_show)} student(s) based on your request")

                # Display filtered students
                for student_name in students_to_show:
                    student_data = next(
                        (s for s in all_student_data if s['name'] == student_name), None)
                    if student_data:
                        display_student(student_data)

                # Prepare context for AI response
                filtered_context = []
                for student_name in students_to_show:
                    student_data = next(
                        (s for s in all_student_data if s['name'] == student_name), None)
                    if student_data:
                        filtered_context.append(
                            f"Name: {student_data['name']}\n"
                            f"Academic Score: {student_data['academic_score']:.2f}%\n"
                            f"Communication Score: {student_data['communication_score']}%\n"
                            f"Tech Readiness: {student_data['tech_readiness']}%\n"
                            f"Communication Readiness: {student_data['comm_readiness']}%\n"
                            f"Final Score: {student_data['overall_score']}%\n"
                            f"Recommendations: {', '.join(student_data['recommendations'])}\n"
                        )

                # Generate AI response
                context = "\n---\n".join(filtered_context)
                with st.spinner("🤔 Generating detailed response..."):
                    answer = ask_question_over_text(llm, context, user_prompt)
                    st.markdown("### 🤖 AI Response")
                    st.write(answer)
            else:
                st.warning(
                    "No students match your criteria or I couldn't understand your request.")
    else:
        # Show all students if no specific prompt
        st.info(f"Showing all {len(all_student_data)} students")
        for student_data in all_student_data:
            display_student(student_data)
