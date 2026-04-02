import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
import os

# =========================
# Configure OpenRouter API
# =========================
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# =========================
# Extract text from PDF
# =========================
def extract_pdf_text(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


# =========================
# Call OpenRouter AI
# =========================
def get_ai_response(job_description, resume_text, prompt):
    full_prompt = f"""
    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Task:
    {prompt}
    """

    response = client.chat.completions.create(
        model="openrouter/auto",  # free model
        messages=[
            {"role": "system", "content": "You are an expert ATS resume evaluator."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="ATS Resume Expert")

st.header("📄 ATS Resume Tracking System")

job_description = st.text_area("Paste Job Description")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)", type=["pdf"]
)

if uploaded_file:
    st.success("Resume uploaded successfully")


# =========================
# Buttons
# =========================
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve My Skills")
submit3 = st.button("Percentage Match")
submit4 = st.button("Show Resume Rating")


# =========================
# Prompts
# =========================
prompt_review = """
Review the resume against the job description.
Highlight strengths and weaknesses of the candidate.
"""

prompt_skills = """
Suggest improvements to the candidate’s skills
based on the job description.
Mention missing skills and learning suggestions.
"""

prompt_match = """
Give:
1. Percentage match between resume and job description
2. Missing keywords
3. Final thoughts
"""

prompt_rating = """
Rate this resume from 1 to 5 stars based on:
- skill alignment
- relevance to the role
- overall quality
Also explain the rating briefly.
"""


# =========================
# Extract resume text
# =========================
resume_text = ""
if uploaded_file:
    resume_text = extract_pdf_text(uploaded_file)


# =========================
# Button Actions
# =========================
if submit1 and uploaded_file:
    response = get_ai_response(
        job_description,
        resume_text,
        prompt_review
    )
    st.subheader("Resume Analysis")
    st.write(response)

elif submit2 and uploaded_file:
    response = get_ai_response(
        job_description,
        resume_text,
        prompt_skills
    )
    st.subheader("Skill Improvement Suggestions")
    st.write(response)

elif submit3 and uploaded_file:
    response = get_ai_response(
        job_description,
        resume_text,
        prompt_match
    )
    st.subheader("ATS Match Result")
    st.write(response)

elif submit4 and uploaded_file:
    response = get_ai_response(
        job_description,
        resume_text,
        prompt_rating
    )
    st.subheader("Resume Rating")
    st.write(response)

elif (submit1 or submit2 or submit3 or submit4) and not uploaded_file:
    st.warning("⚠️ Please upload a resume first.")