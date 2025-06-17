import pandas as pd


def AcademicPerformanceAgent(row):
    score = (
        0.3 * row['attendance'] +
        0.3 * row['test_score'] +
        0.3 * row['assignment_percentage'] +
        (10 if row['event_participation'].strip().lower() == 'yes' else 0)
    )
    reason = f"Score from attendance, tests, assignments, and events."
    return min(100, score), reason


def SoftSkillInsightAgent(bio, resume_text, llm):
    input_text = f"LinkedIn Bio:\n{bio}\n\nResume:\n{resume_text}\n\nEvaluate communication skills (0-100) with reasons:"
    if hasattr(llm, "generate_content"):  # Gemini
        response = llm.generate_content(input_text).text
    else:  # HuggingFace or LangChain-style LLM
        response = llm.invoke(input_text) if hasattr(
            llm, "invoke") else llm(input_text)

        return response


def ReadinessScoringAgent(academic, communication):
    tech = academic
    comm = communication
    overall = int(0.6 * tech + 0.4 * comm)
    return overall, tech, comm


def InterventionRecommenderAgent(overall, tech, comm):
    recs = []
    if overall < 70:
        recs.append("Join a placement bootcamp.")
    if comm < 65:
        recs.append("Attend a resume/communication workshop.")
    if tech < 65:
        recs.append("Practice coding on platforms like LeetCode.")
    return recs or ["You're on track! Keep it up."]
