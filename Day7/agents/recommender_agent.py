def recommend(score_dict):
    score = int(score_dict["final_score"].replace('%', ''))

    if score > 80:
        return "🎉 Ready for placement!"
    elif score > 60:
        return "⚠️ Attend resume & interview workshop."
    else:
        return "🧭 Needs mentoring + mock interviews."
