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

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(uploaded_file):
    if uploaded_file.type == "applications/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    
    return uploaded_file.read().decode("utf-8")

if analyze_button and upload_file:
    try:
        file_content = extract_text_from_txt(upload_file)

        if not file_content.strip():
            st.error("The uploaded file is empty. Please upload a valid PDF or TXT file.")
            st.stop()

        prompt = f"""
        Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}

        Resume content:
        {file_content}

        Provide your analysis in a structured format with clear recommendations.
        """

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides resume critiques."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        st.markdown("### Resume Analysis and Feedback:")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

    try:
        file_content = extract_text_from_txt(upload_file)

        if not file_content.strip():
            st.error("The uploaded file is empty. Please upload a valid PDF or TXT file.")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations."""
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(  
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides resume critiques."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        st.markdown("### Resume Analysis and Feedback:")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")