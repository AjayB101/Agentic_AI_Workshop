from pydantic import BaseModel, Field


class Mcq(BaseModel):
            question:str=Field(description="Question")
            options:list=Field(description="Contains 4 options for the questions A,B,C,D ")
            answer:str=Field(description="Correct answer for the question")