import streamlit as st
import os
import PyPDF2
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Critiquer", page_icon="📃", layout="centered")


st.title("📃 Resume Critiquer")
st.markdown("Upload your resume in PDF format and get instant feedback to improve it!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

upload_file = st.file_uploader("Choose a PDF/TEXT file", type=["pdf", "txt"])

job_role=st.text_input("Enter the job role you are applying for:")

analyze_button = st.button("Analyze Resume")