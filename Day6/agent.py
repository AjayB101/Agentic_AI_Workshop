from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from scorer_tools import academic_score_tool, soft_skills_tool

# 1. LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# 2. Tools
tools = [
    Tool(
        name="AcademicScorer", 
        func=academic_score_tool,
        description="Calculate academic readiness score from academic information string containing attendance, assignment scores, and test scores."
    ),
    Tool(
        name="SoftSkillsScorer", 
        func=soft_skills_tool,
        description="Calculate communication readiness score from soft skills information string containing interview scores, bio quality, faculty feedback, and resume text."
    )
]

system_prompt = """
You are a placement readiness evaluator for college students seeking placements.

Your task:
1. Use the AcademicScorer tool to evaluate technical/academic readiness
2. Use the SoftSkillsScorer tool to evaluate communication readiness
3. Analyze the student's resume and overall profile
4. Provide a comprehensive placement readiness assessment

After using both tools, provide a structured evaluation that includes:
- Technical readiness percentage (from academic metrics)
- Communication readiness percentage (from soft skills metrics)
- Key strengths identified from the resume and scores
- Areas needing improvement
- Specific recommendations (resume bootcamps, peer mentoring, skill development, etc.)
- Intervention flag if student needs immediate support
- Overall placement readiness level (Ready/Needs Improvement/Requires Intervention)

Format your final response as a clear, professional assessment that a placement coordinator would use to guide student development.
"""

# 3. Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Academic Info:\n{academic_info}\n\nSoft Skills Info:\n{soft_skills_info}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# 4. Create agent and executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def evaluate_student(data: dict) -> str:
    """
    Evaluate student placement readiness using the agent.
    """
    academic_info = (
        f"Attendance: {data['attendance']}%\n"
        f"Assignment Score: {data['assignment_score']}%\n"
        f"Test Score: {data['test_score']}%"
    )

    soft_skills_info = (
        f"Mock Interview Score: {data['mock_interview_score']}%\n"
        f"Bio Quality Score: {data['bio_quality_score']}%\n"
        f"Faculty Feedback Score: {data['faculty_feedback_score']}%\n"
        f"Resume: {data.get('resume_text', '(no resume provided)')}"
    )

    try:
        result = agent_executor.invoke({
            "academic_info": academic_info,
            "soft_skills_info": soft_skills_info
        })
        
        # Extract and format the output
        output = result.get("output", "")
        if not output:
            return "Error: No evaluation output generated"
        
        return output
    
    except Exception as e:
        return f"**Error during evaluation:** {str(e)}\n\nPlease check your input data and try again."