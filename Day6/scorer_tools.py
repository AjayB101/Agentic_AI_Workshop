import re

def academic_score_tool(input_string: str) -> str:
    """
    Parse academic information from string input and calculate score.
    Expected format:
    Attendance: 85%
    Assignment Score: 80%
    Test Score: 75%
    """
    try:
        # Extract values using regex
        attendance_match = re.search(r'Attendance:\s*(\d+)%', input_string)
        assignment_match = re.search(r'Assignment Score:\s*(\d+)%', input_string)
        test_match = re.search(r'Test Score:\s*(\d+)%', input_string)
        
        if not all([attendance_match, assignment_match, test_match]):
            return "Error: Could not parse academic information"
        
        attendance = int(attendance_match.group(1))
        assignment_score = int(assignment_match.group(1))
        test_score = int(test_match.group(1))
        
        # Calculate weighted score
        score = (attendance * 0.2 + assignment_score * 0.4 + test_score * 0.4)
        
        # Provide detailed analysis
        analysis = []
        if attendance >= 90:
            analysis.append("Excellent attendance record")
        elif attendance >= 75:
            analysis.append("Good attendance")
        else:
            analysis.append("Poor attendance - needs improvement")
            
        if assignment_score >= 85:
            analysis.append("Strong assignment performance")
        elif assignment_score >= 70:
            analysis.append("Adequate assignment performance")
        else:
            analysis.append("Assignment scores need improvement")
            
        if test_score >= 85:
            analysis.append("Excellent test performance")
        elif test_score >= 70:
            analysis.append("Good test performance")
        else:
            analysis.append("Test scores need significant improvement")
        
        return f"Academic readiness: {round(score, 2)}%. Analysis: {'; '.join(analysis)}"
    
    except Exception as e:
        return f"Error calculating academic score: {str(e)}"

def soft_skills_tool(input_string: str) -> str:
    """
    Parse soft skills information from string input and calculate score.
    Expected format:
    Mock Interview Score: 65%
    Bio Quality Score: 70%
    Faculty Feedback Score: 60%
    Resume: [resume text]
    """
    try:
        # Extract values using regex
        interview_match = re.search(r'Mock Interview Score:\s*(\d+)%', input_string)
        bio_match = re.search(r'Bio Quality Score:\s*(\d+)%', input_string)
        feedback_match = re.search(r'Faculty Feedback Score:\s*(\d+)%', input_string)
        
        if not all([interview_match, bio_match, feedback_match]):
            return "Error: Could not parse soft skills information"
        
        mock_interview_score = int(interview_match.group(1))
        bio_quality_score = int(bio_match.group(1))
        faculty_feedback_score = int(feedback_match.group(1))
        
        # Calculate weighted score
        score = (mock_interview_score * 0.6 + 
                bio_quality_score * 0.2 + 
                faculty_feedback_score * 0.2)
        
        # Check if resume is provided and analyze it
        has_resume = "Resume:" in input_string and "(no resume provided)" not in input_string
        resume_quality_bonus = 0
        resume_analysis = []
        
        if has_resume:
            resume_text = input_string.lower()
            # Basic resume quality indicators
            if any(skill in resume_text for skill in ['javascript', 'python', 'java', 'react', 'node']):
                resume_quality_bonus += 3
                resume_analysis.append("Strong technical skills evident")
            if any(exp in resume_text for exp in ['experience', 'years', 'developed', 'built', 'led']):
                resume_quality_bonus += 2
                resume_analysis.append("Relevant work experience")
            if any(edu in resume_text for edu in ['bachelor', 'engineering', 'computer', 'cgpa', 'gpa']):
                resume_quality_bonus += 1
                resume_analysis.append("Educational background well-documented")
            if any(cert in resume_text for cert in ['certification', 'certified', 'course']):
                resume_quality_bonus += 1
                resume_analysis.append("Additional certifications present")
        else:
            resume_analysis.append("No resume provided - major disadvantage")
        
        # Analyze communication aspects
        comm_analysis = []
        if mock_interview_score >= 80:
            comm_analysis.append("Strong interview performance")
        elif mock_interview_score >= 60:
            comm_analysis.append("Adequate interview skills")
        else:
            comm_analysis.append("Interview skills need significant improvement")
            
        if bio_quality_score >= 80:
            comm_analysis.append("Well-crafted professional bio")
        elif bio_quality_score >= 60:
            comm_analysis.append("Bio needs minor improvements")
        else:
            comm_analysis.append("Bio requires major revision")
            
        if faculty_feedback_score >= 80:
            comm_analysis.append("Excellent faculty feedback")
        elif faculty_feedback_score >= 60:
            comm_analysis.append("Good faculty feedback")
        else:
            comm_analysis.append("Poor faculty feedback - needs attention")
        
        final_score = min(100, score + resume_quality_bonus)  # Cap at 100%
        
        analysis_text = "; ".join(comm_analysis + resume_analysis)
        bonus_text = f" (+{resume_quality_bonus}% resume bonus)" if resume_quality_bonus > 0 else ""
        
        return f"Communication readiness: {round(final_score, 2)}%{bonus_text}. Analysis: {analysis_text}"
    
    except Exception as e:
        return f"Error calculating soft skills score: {str(e)}"