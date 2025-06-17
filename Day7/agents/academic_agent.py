def analyze_academics(student, model):
    prompt = f"""Student Academic Info:
- Attendance: {student['attendance']}%
- Assignments: {student['assignments']}%
- Test Scores: {student['test_scores']}%
- Events Attended: {student['placement_events']}

Rate academic consistency on a scale of 0 to 100 with explanation."""
    return model.invoke(prompt)
