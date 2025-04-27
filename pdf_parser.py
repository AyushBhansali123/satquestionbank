# pdf_parser.py
import fitz  # PyMuPDF
from PIL import Image
import io
import re

def extract_question_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        images.append(img)

    return images

def extract_correct_answers_and_explanations_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    images = []
    answers = []

    for page in doc:
        text += page.get_text()
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        images.append(img)

    matches = re.findall(r'Correct Answer:\s*([A-Z0-9]+)', text)
    for match in matches:
        answers.append(match.strip())

    return answers, images
