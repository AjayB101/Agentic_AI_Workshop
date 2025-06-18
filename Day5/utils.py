from llm_config import LLMConfig
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from parser import Mcq
class Utils:
    def __init__(self):
        self.llm=LLMConfig().get_llm()
    def summarise(self,pdfText):
        prompt = """
        You are an academic assistant. Read the following study material and generate a concise summary in 4–6 bullet points that capture the key concepts and insights.

        Text:
        {pdfText}

        Summary:
        """
        if pdfText:
            summ_temp=PromptTemplate.from_template(template=prompt)
            summ_chain=summ_temp|self.llm
            res=summ_chain.invoke({"pdfText":pdfText})
            return res.content.strip()
            
        else:
            raise ValueError("No data is Extracted from pdf")
        
    def generate_mcqs(self,summary):
        parser=JsonOutputParser(pydantic_object=Mcq)
        prompt = """
        You are a skilled educator tasked with creating multiple-choice questions (MCQs) from academic content.

       {json_format}

        Ensure:
        - Each question is clear and concise.
        - Each question has exactly 4 options (A, B, C, D).
        - The correct answer is indicated by its corresponding letter ("A", "B", "C", or "D").

        Summary:
        {summary}

        Output (as a JSON array of 3 MCQs):
        """

        mcq_temp=PromptTemplate(template=prompt,input_variables=["summary"],partial_variables={"json_format":parser.get_format_instructions()})
        mcq_chain=mcq_temp|self.llm
        mcq_res=mcq_chain.invoke({"summary":summary})
        print(mcq_res.content.strip())
        return mcq_res.content.strip()
        
        

     
        