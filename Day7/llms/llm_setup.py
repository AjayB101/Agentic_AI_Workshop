from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceEndpoint

def get_gemini():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        google_api_key="AIzaSyC764JrVP4Sc5ahEdQEtAgxxwEBmx4DZwQ"
    )

def get_phi():
    return HuggingFaceEndpoint(
        repo_id="microsoft/Phi-3-mini-4k-instruct",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        huggingfacehub_api_token="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"
    )
