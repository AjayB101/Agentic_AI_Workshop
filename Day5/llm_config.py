from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


class LLMConfig:
    def __init__(self):
        load_dotenv()
        self.key=os.getenv("GROQ_API_KEY")
        if not self.key:
            raise ValueError("No Groq api keys")
    def get_llm(self):
       llm=   ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=self.key
             )
       return llm