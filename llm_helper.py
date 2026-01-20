import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Prioritize Streamlit Secrets, then Environment Variables
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Missing GROQ_API_KEY.")
    st.stop()

# UPDATED MODEL NAME HERE
llm = ChatGroq(
    groq_api_key=api_key, 
    model_name='llama-3.3-70b-versatile' 
)