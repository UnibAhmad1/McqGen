# Importing packages
import os
import pandas as pd
import json
import traceback
import PyPDF2                       # type: ignore
from dotenv import load_dotenv
#Importing necessary packages
from langchain_community.llms import HuggingFaceHub # type: ignore
from langchain.prompts import PromptTemplate # type: ignore
from langchain.chains import LLMChain # type: ignore
from langchain.chains import SequentialChain # type: ignore

#load envirment variable
load_dotenv(r"C:\Users\uniba\McqGen\.env")
KEY=os.getenv("HUGGINGFACEHUB_API_TOKEN")

#Using LLM Model from HuggingFaceHub
llm=HuggingFaceHub(
    repo_id = "google/gemma-3-270m",
    model_kwargs={"temperature": 0.7, "max_length": 800},
    huggingfacehub_api_token=KEY
)

#Template for input prompt
Template="""
You are a **master quiz architect** hired to design a dazzling set of {number} multiple-choice questions.

Theme: **{subject}**
Difficulty Target: **{levels}**

Source material for inspiration:
---------------------------------
{text}
---------------------------------

 **Your Mission**
Craft questions that:
1. Spark curiosity and test true understanding—no simple fact-recall.
2. Each question must have exactly 4 distinct options (A–D), with one correct answer.
3. Mix question types: conceptual, application, or a tiny real-world twist when possible.

🖼 **Formatting Canvas**
Respond *only* in valid JSON that matches this exact skeleton:
{response_json}

 Tips for Style
- Make the wrong answers *plausible* to challenge learners.
- Keep language concise and friendly, like a great teacher setting an exciting quiz.
- Vary question openings: “Which statement…”, “What would happen if…”, “Identify the…”, etc.

Deliver a JSON array that a program can parse immediately—no extra commentary.
"""""""""

#Input Prompt
quiz_prompt = PromptTemplate(
    input_variables=["text", "subject", "levels", "number", "response_json"],
    template=Template
)

#Quiz Chain
quiz_chain=LLMChain(llm=llm, prompt=quiz_prompt, output_key="quiz", verbose=True)

Template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
#Review Prompt
quiz_review_prompt=PromptTemplate(
    input_variables=["subject", "quiz"],
    template=Template2
)

#review Chain
review_chain=LLMChain(llm=llm, prompt=quiz_review_prompt, verbose=True, output_key="review")

#Combining both quiz and revview chain by Sequential Chain
generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "subject", "levels", "number", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)