import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

#load json file
with open(r"C:\Users\uniba\McqGen\response.json", 'r') as file:
    RESPONSE_JSON=json.load(file)

#Creating the titile for the webpage
with st.form("MCQ Generator"):
    # File upload
    upload_file=st.file_uploader("Uplaod Your File Either PDF or Text!")

    #Input fields
    mcq_count=st.number_input("No. of MCQ's", min_value=3, max_value=20)

    #Subject
    Subject=st.text_input("Enter the subject", max_chars=20)

    #Level
    Level=st.text_input("Enter the difficult level of question", max_chars=20, placeholder="Simple")

    #Create button
    button=st.form_submit_button("Generate MCQ's")

    #checked if all fields is clicked and all input given

    if button and upload_file and mcq_count and Subject and Level is not None:
        with st.spinner("Loading...."):
            try:
                text=read_file(upload_file)
                response=generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject":Subject,
                        "levels": Level,
                        "response_json": json.dumps(RESPONSE_JSON)
                            }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                st.write(response)