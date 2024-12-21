import pdfplumber
from sentence_transformers import SentenceTransformer, util

# Load the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
        # print("exracted text",text)
    return text

def calculate_similarity(resume_text, job_description):
    """Calculate the similarity score between a resume and a job description."""
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
    return similarity

def screen_resume(pdf_path, job_description):
    """Screen a resume by calculating its relevance to the job description."""
    resume_text = extract_text_from_pdf(pdf_path)
    similarity_score = calculate_similarity(resume_text, job_description)
    return similarity_score
