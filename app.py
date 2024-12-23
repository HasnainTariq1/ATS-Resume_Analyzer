from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
from PIL import Image
import pdf2image
import io
import base64

# Load environment variables from a .env file
load_dotenv()

# Configure the Generative AI API with the API key from environment variables
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to interact with the generative AI model
def model_response(prompt,pdf_content,userinput):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([prompt,pdf_content[0],userinput])
    return response.text

# Function to process uploaded PDF and extract content as base64-encoded image
def get_pdf_content(uploaded_file):

    # Convert the PDF to a list of images (one image per page)
    images=pdf2image.convert_from_bytes(uploaded_file.read())

    first_page=images[0]

    # Convert to bytes 
    image_byte_arr = io.BytesIO()
    first_page.save(image_byte_arr,format="JPEG")
    image_byte_arr=image_byte_arr.getvalue()

    # Create a dictionary representing the PDF content as a base64-encoded image
    pdf_parts = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_byte_arr).decode() #Encode to base64  
        }
    ]
    return pdf_parts
   
# Configure the Streamlit web app    
st.set_page_config("ATS Resume Analyzer")
st.header("ATS Resume Analyzer")

input=st.text_area("Job description",key='input')
uploaded_file=st.sidebar.file_uploader(label='Upload your Resume here......',type=['pdf'])

# Notify the user if a file is uploaded
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons for different functionalities
btn1=st.button('Analyze My Resume')
btn2=st.button("Skill Improvement Suggestions")
btn3=st.button("Job Match Percentage")

# Input prompt for detailed resume analysis
input_prompt1 = """
 You are an experienced Technical Human Resource Manager with extensive expertise in recruitment and talent evaluation. Your task is to thoroughly review the provided resume against the specified job description. Provide a professional assessment by:

 Alignment Evaluation: Share your evaluation on how well the candidate's profile matches the role requirements. 
 Strengths: Highlight the candidate's key strengths and qualifications that align with the job description.
 Weaknesses: Identify areas where the candidate's profile falls short or needs improvement in relation to the job requirements..
"""

# Input prompt for ATS evaluation and keyword optimization
input_prompt2 = """
You are a proficient ATS (Applicant Tracking System) scanner with a comprehensive understanding of ATS functionality and recruitment processes. Your task is to evaluate the provided resume against the given job description. Provide the output in the following format:

1. Percentage Match: Calculate and present the percentage that represents how well the resume aligns with the job description.
2. Missing Keywords: Identify and list the important keywords or phrases from the job description that are not present in the resume.
3. Final Thoughts: Summarize the overall evaluation by highlighting the resume's strengths and weaknesses relative to the job description, and provide actionable suggestions for improvement.
Leverage your expertise in ATS algorithms and keyword optimization to deliver an accurate and detailed analysis.
"""

# Input prompt for percentage match only
input_prompt3 = """
how much percentage the resume matches the provide job description . only give the output as Your resume aligns with the job description with an percentage match.
"""

# Handle button's click
if btn1:
    if not input.strip():
        st.write("Please provide a job description before proceeding!")
    elif uploaded_file is not None:
        pdfContent=get_pdf_content(uploaded_file)
        response=model_response(input,pdfContent,input_prompt1)
        st.header("Response....")
        st.write(response)
    
    else:
        st.write("Please upload your file")

elif btn2:
    if not input.strip():
        st.write("Please provide a job description before proceeding!")
    elif uploaded_file is not None:
        pdfContent=get_pdf_content(uploaded_file)
        response=model_response(input,pdfContent,input_prompt2)
        st.header("Response....")
        st.write(response)
    else:
        st.write("Please upload your file")
    

elif btn3:
    if not input.strip():
        st.write("Please provide a job description before proceeding!")
    elif uploaded_file is not None:
        pdfContent=get_pdf_content(uploaded_file)
        response=model_response(input,pdfContent,input_prompt3)
        st.header("Response....")
        st.write(response)
    
    else:
        st.write("Please upload your file")