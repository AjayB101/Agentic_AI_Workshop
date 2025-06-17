import os
from langchain_community.llms import HuggingFaceEndpoint
import google.generativeai as genai

# Setup Gemini


def get_gemini_llm():
    genai.configure(api_key="AIzaSyC764JrVP4Sc5ahEdQEtAgxxwEBmx4DZwQ")
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

# Setup HuggingFace Phi-3


def get_phi_llm():
    return HuggingFaceEndpoint(
        repo_id="microsoft/Phi-3-mini-4k-instruct",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        huggingfacehub_api_token=os.getenv(
            "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"),
    )
