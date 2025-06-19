import PyPDF2
import docx
import tempfile


def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        return extract_text_from_doc_or_txt(file)
    else:
        return ""


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())


def extract_text_from_doc_or_txt(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    else:  # docx
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            doc = docx.Document(tmp.name)
            return "\n".join([p.text for p in doc.paragraphs])


def ask_question_over_text(llm, text, question):
    prompt = f"Context:\n{text}\n\nQuestion: {question}\nAnswer:"

    # Handle different LLM types
    if hasattr(llm, "generate_content"):  # Gemini
        response = llm.generate_content(prompt)
        return response.text
    elif hasattr(llm, "invoke"):  # LangChain-style LLM
        return llm.invoke(prompt)
    else:  # Direct callable
        return llm(prompt)


def analyze_prompt_for_filtering(llm, all_student_data, user_prompt):
    """Use AI to determine which students to show based on the prompt"""

    # Create a summary of all students for AI analysis
    student_summary = []
    for student in all_student_data:
        student_summary.append(
            f"- {student['name']}: Overall Score {student['overall_score']}%, "
            f"Academic {student['academic_score']:.1f}%, Communication {student['communication_score']}%"
        )

    analysis_prompt = f"""
You are analyzing a user request about student placement readiness scores. 

Available Students:
{chr(10).join(student_summary)}

User Request: "{user_prompt}"

Based on the user's request, determine which students should be shown. Return ONLY a comma-separated list of student names to display, or "ALL" if all students should be shown.

Examples:
- "Show students below 70%" → return names of students with overall score < 70%
- "How can Neha Sharma improve?" → return "Neha Sharma"
- "Who are the top performers?" → return names of students with highest scores
- "Students with communication issues" → return names of students with low communication scores
- "Show all students" → return "ALL"

Response format: Just the names separated by commas (e.g., "Neha Sharma, Avni Mehta") or "ALL"
"""

    try:
        if hasattr(llm, "generate_content"):  # Gemini
            response = llm.generate_content(analysis_prompt)
            result = response.text.strip()
        elif hasattr(llm, "invoke"):  # LangChain-style LLM
            result = llm.invoke(analysis_prompt).strip()
        else:
            result = llm(analysis_prompt).strip()

        if result.upper() == "ALL":
            return [student['name'] for student in all_student_data]
        else:
            # Parse the comma-separated names
            student_names = [name.strip()
                             for name in result.split(',') if name.strip()]
            # Validate that these students exist
            valid_names = [student['name'] for student in all_student_data]
            filtered_names = [
                name for name in student_names if name in valid_names]
            return filtered_names if filtered_names else [student['name'] for student in all_student_data]

    except Exception as e:
        print(f"Error in AI filtering: {e}")
        # Fallback: return all students
        return [student['name'] for student in all_student_data]
