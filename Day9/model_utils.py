import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import google.generativeai as genai


def get_gemini_llm():
    """Get Gemini LLM for LangChain"""
    api_key = "AIzaSyDGrDdgXB-E8atDoZalaNXVulK4CCBihQY"  # Replace with your actual API key
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.3,
        convert_system_message_to_human=True
    )


def get_phi_llm():
    """Get Phi-3 LLM for LangChain"""
    return HuggingFaceEndpoint(
        repo_id="microsoft/Phi-3-mini-4k-instruct",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        huggingfacehub_api_token="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"
    )


# Prompt Templates
ACADEMIC_SCORING_PROMPT = PromptTemplate(
    input_variables=["attendance", "test_score",
                     "assignment_percentage", "event_participation"],
    template="""
    You are an Academic Performance Evaluation Agent. Analyze the student's academic data and provide a score.

    Student Academic Data:
    - Attendance: {attendance}%
    - Test Score: {test_score}%
    - Assignment Completion: {assignment_percentage}%
    - Event Participation: {event_participation}

    Calculate an academic performance score out of 100 based on:
    - Attendance (30% weight)
    - Test Score (30% weight)
    - Assignment Completion (30% weight)
    - Event Participation (10% bonus if 'yes')

    Provide your response in this exact format:
    SCORE: [numerical score]
    REASONING: [brief explanation of the scoring]
    """
)

SOFT_SKILLS_PROMPT = PromptTemplate(
    input_variables=["linkedin_bio", "resume_text"],
    template="""
    You are a Soft Skills Evaluation Agent. Analyze the student's professional profile and evaluate their communication skills.

    LinkedIn Bio:
    {linkedin_bio}

    Resume Text:
    {resume_text}

    Evaluate the communication skills and professional readiness based on:
    - Quality of written communication
    - Professional presentation
    - Clarity and coherence
    - Professional experience indicators

    Provide a score out of 100 and explain your reasoning.

    Provide your response in this exact format:
    SCORE: [numerical score]
    REASONING: [detailed explanation of the communication skills assessment]
    """
)

READINESS_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["academic_score", "communication_score", "student_name"],
    template="""
    You are a Placement Readiness Analysis Agent. Calculate the overall placement readiness for {student_name}.

    Scores:
    - Academic Score: {academic_score}%
    - Communication Score: {communication_score}%

    Calculate the overall readiness using:
    - Technical Readiness = Academic Score
    - Communication Readiness = Communication Score  
    - Overall Readiness = (Technical × 0.6) + (Communication × 0.4)

    Provide your response in this exact format:
    OVERALL_SCORE: [numerical score]
    TECH_READINESS: [technical readiness score]
    COMM_READINESS: [communication readiness score]
    ANALYSIS: [brief analysis of the student's placement readiness]
    """
)

INTERVENTION_PROMPT = PromptTemplate(
    input_variables=["overall_score", "tech_score",
                     "comm_score", "student_name"],
    template="""
    You are an Intervention Recommendation Agent. Provide specific recommendations for {student_name} to improve their placement readiness.

    Current Scores:
    - Overall Score: {overall_score}%
    - Technical Readiness: {tech_score}%
    - Communication Readiness: {comm_score}%

    Based on these scores, provide specific, actionable recommendations. Consider:
    - If overall < 70%: Suggest comprehensive improvement strategies
    - If communication < 65%: Focus on communication skills development
    - If technical < 65%: Focus on technical skills improvement
    - If scores are good: Provide maintenance and enhancement suggestions

    Provide 3-5 specific, actionable recommendations.

    Format your response as:
    RECOMMENDATIONS:
    1. [specific recommendation]
    2. [specific recommendation]
    3. [specific recommendation]
    [additional recommendations if needed]
    """
)

QUERY_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["user_query", "available_students"],
    template="""
    You are a Query Analysis Agent. Analyze the user's request and determine which students should be shown.

    Available Students:
    {available_students}

    User Query: "{user_query}"

    Analyze the query and determine which students match the criteria. Consider:
    - Performance-based filters (e.g., "below 70%", "top performers")
    - Specific student names
    - Skill-based queries (e.g., "communication issues", "technical problems")
    - General requests (e.g., "show all", "everyone")

    Respond with ONLY the student names that match, separated by commas, or "ALL" if all students should be shown.

    Examples:
    - "Show students below 70%" → return names of students with overall score < 70%
    - "How can John improve?" → return "John"
    - "Top performers" → return names of highest scoring students
    - "All students" → return "ALL"

    Response: [comma-separated names or "ALL"]
    """
)

RAG_RESPONSE_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are a Placement Readiness Assistant. Use the provided student data to answer the user's question comprehensively.

    Student Data Context:
    {context}

    User Question: {question}

    Provide a detailed, helpful response based on the student data. Include:
    - Direct answers to the question
    - Relevant insights from the data
    - Specific recommendations when appropriate
    - Comparative analysis when relevant

    Be conversational and helpful while being accurate and data-driven.

    Response:
    """
)
