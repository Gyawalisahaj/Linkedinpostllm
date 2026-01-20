# Linkedinpostllm
**Automated LinkedIn Post Generator**
LinkedIn Post Generator built using LangChain and Large Language Models (LLMs) to create engaging, professional, and personalized LinkedIn posts from minimal user input.
---

## ✨ Features
* **Style Learning**: Extracts writing patterns from your previous posts to maintain brand consistency.
* **Automated Metadata**: Automatically calculates line counts and categorizes post length (Short, Medium, Long).
* **Tag Unification**: Uses LLMs to clean and unify messy tags into professional categories.
* **Smart Filtering**: Filter examples by Language (English/Nepali), Length, and Topic (e.g., "Job Search").
* **Streamlit UI**: A clean, interactive dashboard for one-click post generation.

---

## 🛠️ Tech Stack
* **LLM**: Groq (Llama-3.3-70b-versatile)
* **Orchestration**: LangChain
* **Framework**: Streamlit
* **Data Processing**: Pandas & JSON
* **Environment**: Python 3.12+ (Optimized for Fedora Linux)

---

## Requirements 
streamlit>=1.35.0
langchain-groq>=0.1.0
python-dotenv>=1.0.1
pandas>=2.2.3
langchain-core>=0.2.0


## To RUN 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt