import streamlit as st
import fitz  # PyMuPDF
from google import genai

# Configure Gemini API
client = genai.Client(api_key="AIzaSyCvOToKUYmHQI1Ecc8TQ6byWSFPF1HmJWw")

# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


# Function to call Gemini
def get_gemini_response(job_description, resume_text, prompt):
    full_prompt = f"""
    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Task:
    {prompt}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt
    )

    return response.text


# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")

st.header("📄 ATS Resume Tracking System")

job_description = st.text_area("Paste Job Description")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)", type=["pdf"]
)

if uploaded_file:
    st.success("Resume uploaded successfully")

# Buttons
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve My Skills")
submit3 = st.button("Percentage Match")
submit4 = st.button("Show Resume Rating")

# Prompts
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

# Extract resume text
if uploaded_file:
    resume_text = extract_pdf_text(uploaded_file)

# Button actions
if submit1 and uploaded_file:
    response = get_gemini_response(
        job_description,
        resume_text,
        prompt_review
    )
    st.subheader("Resume Analysis")
    st.write(response)

elif submit2 and uploaded_file:
    response = get_gemini_response(
        job_description,
        resume_text,
        prompt_skills
    )
    st.subheader("Skill Improvement Suggestions")
    st.write(response)

elif submit3 and uploaded_file:
    response = get_gemini_response(
        job_description,
        resume_text,
        prompt_match
    )
    st.subheader("ATS Match Result")
    st.write(response)

elif submit4 and uploaded_file:
    response = get_gemini_response(
        job_description,
        resume_text,
        prompt_rating
    )
    st.subheader("Resume Rating")
    st.write(response)