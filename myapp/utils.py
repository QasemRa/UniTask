import os
import tempfile
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Try extracting text directly
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")

    # If no text extracted, use OCR
    if not text.strip():
        try:
            images = convert_from_path(pdf_path)
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
        except Exception as e:
            print(f"Error with OCR: {e}")

    return text.strip()

def compute_similarity(texts):
    if len(texts) < 2:
        return []

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    results = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            similarity = round(similarity_matrix[i][j] * 100, 1)
            if similarity > 10:  # Threshold
                results.append({
                    'text1_index': i,
                    'text2_index': j,
                    'similarity': similarity
                })

    return results
