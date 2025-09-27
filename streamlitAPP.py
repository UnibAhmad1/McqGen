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

        if isinstance(response, dict):
            # Extract the quiz data safely
            quiz = response.get("quiz", "")

            if quiz:
                table_data=get_table_data(quiz)
                if table_data:
                    df=pd.DataFrame(table_data)
                    df.index=df.index+1
                    st.table(df)
                    # Display the review in a text area
                    st.text_area(label="Review", value=response.get("review", ""))
                else:
                    st.error("Error in the table data")
            else:
                st.error("Could not parse quiz JSON from AI output")
        else:
            st.write(response)
# import os
# import json
# import traceback
# import pandas as pd
# from dotenv import load_dotenv
# from src.mcqgenerator.utils import read_file,get_table_data
# import streamlit as st
# from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

# import re, json

# # Post-processing function to extract JSON from TinyLlama output
# def extract_quiz_json(raw_text):
#     """
#     Tries to find a JSON object inside raw text returned by TinyLlama.
#     Returns dict if successful, else empty dict.
#     """
#     match = re.search(r"\{.*\}", raw_text, re.S)  # search for {...} including newlines
#     if match:
#         try:
#             return json.loads(match.group())
#         except json.JSONDecodeError:
#             return {}
#     return {}

# #load json file
# with open(r"C:\Users\uniba\McqGen\response.json", 'r') as file:
#     RESPONSE_JSON=json.load(file)

# #Creating the titile for the webpage
# with st.form("MCQ Generator"):
#     # File upload
#     upload_file=st.file_uploader("Uplaod Your File Either PDF or Text!")

#     #Input fields
#     mcq_count=st.number_input("No. of MCQ's", min_value=3, max_value=20)

#     #Subject
#     Subject=st.text_input("Enter the subject", max_chars=20)

#     #Level
#     Level=st.text_input("Enter the difficult level of question", max_chars=20, placeholder="Simple")

#     #Create button
#     button=st.form_submit_button("Generate MCQ's")

#     #checked if all fields is clicked and all input given

#     if button and upload_file and mcq_count and Subject and Level is not None:
#         with st.spinner("Loading...."):
#             try:
#                 text=read_file(upload_file)
#                 response=generate_evaluate_chain(
#                         {
#                         "text": text,
#                         "number": mcq_count,
#                         "subject":Subject,
#                         "levels": Level,
#                         "response_json": json.dumps(RESPONSE_JSON)
#                             }
#                     )
#             except Exception as e:
#                 traceback.print_exception(type(e), e, e.__traceback__)
#                 st.error("Error")

#         if isinstance(response, dict):
#                 #Extract the quiz data from the response
#                 raw_quiz = response.get("quiz", "")
#                 quiz = extract_quiz_json(raw_quiz)
#                 if quiz is not None:
#                         table_data=get_table_data(quiz)
#                         if table_data is not None:
#                                 df=pd.DataFrame(table_data)
#                                 df.index=df.index+1
#                                 st.table(df)
#                                 #Display the review in atext box as well
#                                 st.text_area(label="Review", value=response["review"])
#                         else:
#                             st.error("Error in the table data")

#                 else:
#                     st.write(response)


#                 quiz_dict = response.get("quiz", {})  # already a dict

#                 quiz_table_data = []
#                 for key, value in quiz_dict.items():
#                     mcq = value.get("mcq", "")
#                     options = " | ".join(
#                         [f"{option}: {option_value}" for option, option_value in value.get("options", {}).items()]
#                     )
#                     correct = value.get("correct", "")
#                     quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

#                 if quiz_table_data:
#                     df = pd.DataFrame(quiz_table_data)
#                     df.index = df.index + 1
#                     st.table(df)
#                 else:
#                     st.error("No quiz data available")


# import os
# import json
# import traceback
# import pandas as pd
# from dotenv import load_dotenv
# from src.mcqgenerator.utils import read_file
# import streamlit as st
# from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
# import re

# # Post-processing function to extract JSON from TinyLlama output
# def extract_quiz_json(raw_text):
#     """
#     Tries to find a JSON object inside raw text returned by TinyLlama.
#     Returns dict if successful, else empty dict.
#     """
#     match = re.search(r"\{.*\}", raw_text, re.S)  # search for {...} including newlines
#     if match:
#         try:
#             return json.loads(match.group())
#         except json.JSONDecodeError:
#             return {}
#     return {}

# # Load json file
# with open(r"C:\Users\uniba\McqGen\response.json", 'r') as file:
#     RESPONSE_JSON = json.load(file)

# # Creating the title for the webpage
# with st.form("MCQ Generator"):
#     # File upload
#     upload_file = st.file_uploader("Upload Your File (PDF or Text)")

#     # Input fields
#     mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=20)
#     Subject = st.text_input("Enter the subject", max_chars=20)
#     Level = st.text_input("Enter the difficulty level of question", max_chars=20, placeholder="Simple")

#     # Create button
#     button = st.form_submit_button("Generate MCQs")

#     if button and upload_file and mcq_count and Subject and Level:
#         with st.spinner("Generating MCQs..."):
#             try:
#                 text = read_file(upload_file)
#                 response = generate_evaluate_chain({
#                     "text": text,
#                     "number": mcq_count,
#                     "subject": Subject,
#                     "levels": Level,
#                     "response_json": json.dumps(RESPONSE_JSON)
#                 })
#             except Exception as e:
#                 traceback.print_exception(type(e), e, e.__traceback__)
#                 st.error("Error while generating MCQs")
#                 response = {}

#         # Process the response
#         if isinstance(response, dict):
#             raw_quiz = response.get("quiz", "")
#             quiz_dict = extract_quiz_json(raw_quiz)  # returns dict or empty dict

#             quiz_table_data = []
#             for key, value in quiz_dict.items():
#                 mcq = value.get("mcq", "")
#                 options = " | ".join(
#                     [f"{option}: {option_value}" for option, option_value in value.get("options", {}).items()]
#                 )
#                 correct = value.get("correct", "")
#                 quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

#             if quiz_table_data:
#                 df = pd.DataFrame(quiz_table_data)
#                 df.index = df.index + 1
#                 st.table(df)
#                 # Display review text
#                 st.text_area(label="Review", value=response.get("review", ""))
#             else:
#                 st.error("No quiz data available or AI output could not be parsed correctly.")

