import streamlit as st
import pandas as pd
from rag_utils import RAGSystem
from data_base_utils import StudentDatabase
import os

# Page configuration
st.set_page_config(
    page_title="🎓 AI-Powered Placement Readiness System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize RAG system


@st.cache_resource
def initialize_rag_system():
    return RAGSystem()


# Initialize the system
rag_system = initialize_rag_system()

# Title and Header
st.title("🎓 AI-Powered Placement Readiness System")
st.markdown("### Multi-Agent AI System with Persistent ChromaDB Storage")

# Sidebar for database management
with st.sidebar:
    st.header("📊 Database Management")

    # Database stats
    stats = rag_system.get_database_stats()
    st.metric("Total Students", stats.get("total_students", 0))

    # Clear database button
    if st.button("🗑️ Clear Database", type="secondary"):
        rag_system.clear_database()
        st.success("Database cleared!")
        st.rerun()

    st.markdown("---")

    # File upload section
    st.header("📁 Data Upload")
    csv_file = st.file_uploader("Upload Student CSV", type="csv")

    if csv_file is not None:
        if st.button("💾 Load Data to Database"):
            with st.spinner("Loading data to ChromaDB..."):
                df = pd.read_csv(csv_file)
                success = rag_system.load_dataframe_data(df)

                if success:
                    st.success(
                        f"Successfully loaded {len(df)} students to database!")
                    st.rerun()
                else:
                    st.error("Failed to load data to database")

        # Preview data
        if st.checkbox("👀 Preview Data"):
            df = pd.read_csv(csv_file)
            st.dataframe(df.head())

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🤖 AI Query Interface")

    # Query input
    user_prompt = st.text_area(
        "Ask about student placement readiness:",
        placeholder="Examples:\n• Show students below 70%\n• How can John Smith improve?\n• Who are the top performers?\n• Students with communication issues\n• Show all students",
        height=100
    )

    # Query modes
    query_mode = st.radio(
        "Query Mode:",
        ["🎯 Smart Filter & Analysis", "🔍 Semantic Search", "📊 Show All Students"],
        horizontal=True
    )

with col2:
    st.header("ℹ️ System Info")
    st.info("""
    **Multi-Agent System:**
    - 🧠 Academic Performance Agent
    - 💬 Soft Skills Agent  
    - 📈 Readiness Analysis Agent
    - 🎯 Intervention Agent
    - 🔍 Query Analysis Agent
    - 💡 RAG Response Agent
    
    **Features:**
    - Persistent ChromaDB storage
    - LangChain prompt templates
    - Semantic search capabilities
    - AI-powered filtering
    """)

# Process queries
if st.button("🚀 Generate Analysis", type="primary") and user_prompt:
    if stats.get("total_students", 0) == 0:
        st.warning(
            "⚠️ No student data in database. Please upload CSV data first.")
    else:
        with st.spinner("🔄 Processing with Multi-Agent AI System..."):
            try:
                if query_mode == "🔍 Semantic Search":
                    # Semantic search mode
                    students = rag_system.search_and_process_students(
                        user_prompt, n_results=10)
                    st.info(
                        f"Found {len(students)} students using semantic search")

                elif query_mode == "📊 Show All Students":
                    # Show all students
                    students = rag_system.process_all_students()
                    st.info(f"Showing all {len(students)} students")

                else:
                    # Smart filter mode (default)
                    students = rag_system.filter_students_by_query(user_prompt)
                    st.info(
                        f"Smart filter identified {len(students)} relevant students")

                if students:
                    # Display students
                    st.markdown("## 📋 Student Analysis Results")

                    for i, student in enumerate(students):
                        with st.expander(f"👨‍🎓 {student['name']} - Overall Score: {student['overall_score']}%",
                                         expanded=(i < 3)):  # Expand first 3 students

                            # Metrics row
                            col1, col2, col3, col4 = st.columns(4)

                            with col1:
                                st.metric(
                                    "🎯 Overall Readiness",
                                    f"{student['overall_score']}%",
                                    delta=f"{student['overall_score'] - 70}%" if student['overall_score'] != 70 else None
                                )

                            with col2:
                                st.metric(
                                    "📚 Academic Score",
                                    f"{student['academic_score']:.1f}%"
                                )

                            with col3:
                                st.metric(
                                    "💬 Communication",
                                    f"{student['communication_score']}%"
                                )

                            with col4:
                                # Status indicator
                                if student['overall_score'] >= 80:
                                    st.success("🟢 Excellent")
                                elif student['overall_score'] >= 70:
                                    st.warning("🟡 Good")
                                else:
                                    st.error("🔴 Needs Improvement")

                            # Detailed breakdown
                            st.markdown("**📊 Detailed Analysis:**")
                            st.write(
                                f"• **Academic Reasoning:** {student['academic_reasoning']}")
                            st.write(
                                f"• **Communication Assessment:** {student['communication_reasoning']}")
                            st.write(
                                f"• **Overall Analysis:** {student['analysis']}")

                            # Recommendations
                            st.markdown("**💡 Personalized Recommendations:**")
                            for j, rec in enumerate(student['recommendations'], 1):
                                st.write(f"{j}. {rec}")

                    # Generate AI Response
                    st.markdown("## 🤖 AI Assistant Response")
                    with st.spinner("Generating comprehensive AI response..."):
                        ai_response = rag_system.generate_response(
                            students, user_prompt)
                        st.markdown(ai_response)

                    # Summary statistics
                    if len(students) > 1:
                        st.markdown("## 📈 Summary Statistics")

                        avg_overall = sum(s['overall_score']
                                          for s in students) / len(students)
                        avg_academic = sum(s['academic_score']
                                           for s in students) / len(students)
                        avg_comm = sum(s['communication_score']
                                       for s in students) / len(students)

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("📊 Average Overall",
                                      f"{avg_overall:.1f}%")
                        with col2:
                            st.metric("📚 Average Academic",
                                      f"{avg_academic:.1f}%")
                        with col3:
                            st.metric("💬 Average Communication",
                                      f"{avg_comm:.1f}%")
                        with col4:
                            high_performers = len(
                                [s for s in students if s['overall_score'] >= 80])
                            st.metric("🏆 High Performers",
                                      f"{high_performers}/{len(students)}")

                else:
                    st.warning("No students found matching your criteria.")

            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
                st.error("Please check your data format and try again.")

# Show sample data format
elif stats.get("total_students", 0) == 0:
    st.markdown("## 📋 Sample CSV Format")
    st.markdown("Upload a CSV file with the following columns:")

    sample_data = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith'],
        'attendance': [85, 92],
        'test_score': [78, 88],
        'assignment_percentage': [90, 85],
        'event_participation': ['Yes', 'No'],
        'softskill_score': [75, 80],
        'linkedin_bio': ['Software developer with 2 years experience', 'Data analyst passionate about ML'],
        'resume_text': ['Experience in Python and web development', 'Strong background in statistics and analytics']
    })

    st.dataframe(sample_data)

    with st.expander("📝 Column Descriptions"):
        st.markdown("""
        - **name**: Student's full name
        - **attendance**: Attendance percentage (0-100)
        - **test_score**: Average test score percentage (0-100)
        - **assignment_percentage**: Assignment completion percentage (0-100)
        - **event_participation**: Whether student participates in events ('Yes'/'No')
        - **softskill_score**: Initial soft skills assessment score (0-100)
        - **linkedin_bio**: Student's LinkedIn biography (optional)
        - **resume_text**: Resume summary text (optional)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🤖 Powered by Multi-Agent AI System | 🗄️ ChromaDB Persistent Storage | 🔗 LangChain Framework
</div>
""", unsafe_allow_html=True)
