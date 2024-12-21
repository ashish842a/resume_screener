import pdfplumber
import easyocr
import os
from pdf2image import convert_from_path
from sentence_transformers import SentenceTransformer, util

# Load the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize EasyOCR Reader
ocr_reader = easyocr.Reader(['en'])

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF. If pdfplumber fails, convert PDF to image and try using EasyOCR."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Attempt to extract text from PDF using pdfplumber
            text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
            if text:
                return text
            else:
                print("No text found using pdfplumber, converting PDF to image and using EasyOCR...")
                return extract_text_from_pdf_as_image(pdf_path)  # Fallback to EasyOCR after converting PDF to image
    except Exception as e:
        print(f"Error extracting text from PDF using pdfplumber: {str(e)}")
        print("Converting PDF to image and using EasyOCR...")
        return extract_text_from_pdf_as_image(pdf_path)  # Fallback to EasyOCR after converting PDF to image

def extract_text_from_pdf_as_image(pdf_path):
    """Convert PDF to images and use EasyOCR to extract text."""
    try:
        # Convert each page of the PDF to an image using pdf2image
        images = convert_from_path(pdf_path)
        text = ''
        for image in images:
            # Use EasyOCR to extract text from each image
            result = ocr_reader.readtext(image)
            # Combine all text extracted from the image
            text += ' '.join([item[1] for item in result])
        
        return text if text else None
    except Exception as e:
        print(f"Error extracting text from PDF as image: {str(e)}")
        return None

def extract_text_from_image(image_path):
    """Extract text content from an image (JPG, JPEG, PNG) using EasyOCR."""
    try:
        result = ocr_reader.readtext(image_path)
        # Combine all text extracted from the image
        text = ' '.join([item[1] for item in result])
        # print("text using easyicr",text)
        return text if text else None
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return None

def extract_text(file_path):
    """Extract text from either a PDF or an image (JPG, JPEG, PNG)."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(file_path)
    else:
        print("Unsupported file type.")
        return None

def calculate_similarity(resume_text, job_description):
    """Calculate the similarity score between a resume and a job description."""
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
    return similarity

def screen_resume(file_path, job_description):
    """Screen a resume by calculating its relevance to the job description."""
    resume_text = extract_text(file_path)
    
    if resume_text is None:
        return "Error: Unable to extract text from resume."

    similarity_score = calculate_similarity(resume_text, job_description)
    return similarity_score
