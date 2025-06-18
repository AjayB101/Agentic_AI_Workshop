# ReAct Web Research Agent for "AI in Healthcare"
# Using Gemini API and Tavily for web search

import os
import google.generativeai as genai
import requests
from typing import List

# --------- SETUP ---------
# Load API keys (set your Gemini and Tavily keys as environment variables)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Configure Gemini
if not GEMINI_API_KEY:
    raise Exception("Gemini API key not set")
genai.configure(api_key=GEMINI_API_KEY)

# --------- AGENT CLASS ---------
class WebResearchAgent:
    def __init__(self, topic: str):
        self.topic = topic
        self.questions = []
        self.results = {}

    def generate_questions(self):
        prompt = f"""
        Generate 5 to 6 important research questions about the topic: "{self.topic}".
        Cover different angles such as causes, impact, applications, risks, and future directions.
        """
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        self.questions = [q for q in response.text.strip().split("\n") if q.strip()]

    def search_web(self, query: str) -> List[str]:
        url = "https://api.tavily.com/search"
        headers = {"Content-Type": "application/json"}
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": 5
        }
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        return [item["content"] for item in data.get("results", [])]

    def gather_info(self):
        for q in self.questions:
            self.results[q] = self.search_web(q)

    def compile_report(self) -> str:
        report = f"# AI in Healthcare\n\n"
        report += f"## Introduction\nAI is transforming the healthcare industry in profound ways. This report explores several key aspects of how AI is influencing healthcare.\n\n"
        for q in self.questions:
            report += f"### {q}\n"
            if self.results.get(q):
                for bullet in self.results[q]:
                    report += f"- {bullet.strip()}\n"
            else:
                report += "- No data found.\n"
            report += "\n"
        report += "## Conclusion\nAI in healthcare holds great promise, but it also brings ethical and technical challenges. Continuous research and governance are essential to ensure its effective and responsible use."
        return report

# --------- MAIN EXECUTION ---------
if __name__ == "__main__":
    agent = WebResearchAgent("AI in Healthcare")
    print("\n[1] Generating questions using Gemini...")
    agent.generate_questions()
    print("Questions generated:")
    for q in agent.questions:
        print("-", q)

    print("\n[2] Searching the web using Tavily...")
    agent.gather_info()

    print("\n[3] Compiling final report...\n")
    final_report = agent.compile_report()
    with open("ai_in_healthcare_report.md", "w") as f:
        f.write(final_report)
    print("✅ Report saved as ai_in_healthcare_report.md")