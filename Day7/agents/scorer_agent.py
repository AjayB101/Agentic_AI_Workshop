def generate_score(academic_eval, softskill_eval):
    import re

    def extract_score(text):
        match = re.search(r"(\d{1,3})", text)
        return int(match.group()) if match else 0

    academic_score = extract_score(academic_eval)
    soft_score = extract_score(softskill_eval)

    return {
        "tech_ready": f"{academic_score}%",
        "communication_ready": f"{soft_score}%",
        "final_score": f"{(academic_score + soft_score)//2}%"
    }
