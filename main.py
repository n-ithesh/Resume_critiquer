import streamlit as st
import os
import PyPDF2
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Critiquer", page_icon="📃", layout="centered")


