from utils.rag_utils import CSVRetriever

def analyze_softskills(student, model):
    retriever = CSVRetriever("data/sample_benchmark.csv")
    bio = student["linkedin_bio"]
    similar = retriever.query_similar(bio)

    prompt = f"""Student Bio: {bio}
Compare with: {similar}
Rate communication and soft skill readiness out of 100 and explain briefly."""

    return model.invoke(prompt)
