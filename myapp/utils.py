import os
import tempfile
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set the path to the new Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def preprocess_image_for_ocr(image):
    """Simple preprocessing for modern Tesseract version"""
    return image

def extract_text_from_pdf(pdf_path):
    """Enhanced text extraction with better support for Word-to-PDF files"""
    text = ""
    
    # Enhanced text extraction for regular PDFs (especially Word-to-PDF)
    try:
        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages):
            # Method 1: Standard text extraction
            extracted = page.extract_text()
            if extracted and extracted.strip():
                text += f"\n--- Page {page_num + 1} (Standard) ---\n{extracted}\n"
            
            # Method 2: Try get_text method (better for some PDFs)
            try:
                if hasattr(page, 'get_text'):
                    alt_text = page.get_text()
                    if alt_text and alt_text.strip() and alt_text != extracted:
                        text += f"\n--- Page {page_num + 1} (Alternative) ---\n{alt_text}\n"
            except:
                pass
            
            # Method 3: Try extract_text with different parameters
            try:
                if hasattr(page, 'extract_text'):
                    param_text = page.extract_text(extraction_mode="layout")
                    if param_text and param_text.strip() and param_text != extracted:
                        text += f"\n--- Page {page_num + 1} (Layout) ---\n{param_text}\n"
            except:
                pass
                
    except Exception as e:
        print(f"Error extracting text with pypdf: {e}")

    # If we got good text from standard methods, prioritize it
    standard_text = text.strip()
    if len(standard_text) > 100:  # If we got substantial text
        return standard_text
    
    # Otherwise, try OCR as fallback
    try:
        # Convert PDF to images with high DPI for better OCR
        images = convert_from_path(pdf_path, dpi=400)
        
        for i, image in enumerate(images):
            extracted_texts = []
            
            # Configuration 1: Best for general text
            try:
                general_text = pytesseract.image_to_string(
                    image,
                    config='--psm 6 --oem 3'
                )
                if general_text.strip():
                    extracted_texts.append(general_text)
            except:
                pass
            
            # Configuration 2: Best for handwritten text
            try:
                handwritten_text = pytesseract.image_to_string(
                    image,
                    config='--psm 11 --oem 3'
                )
                if handwritten_text.strip() and handwritten_text not in extracted_texts:
                    extracted_texts.append(handwritten_text)
            except:
                pass
            
            # Configuration 3: Sparse text (excellent for handwritten)
            try:
                sparse_text = pytesseract.image_to_string(
                    image,
                    config='--psm 13 --oem 3'
                )
                if sparse_text.strip() and sparse_text not in extracted_texts:
                    extracted_texts.append(sparse_text)
            except:
                pass
            
            # Configuration 4: Single column text
            try:
                single_col_text = pytesseract.image_to_string(
                    image,
                    config='--psm 1 --oem 3'
                )
                if single_col_text.strip() and single_col_text not in extracted_texts:
                    extracted_texts.append(single_col_text)
            except:
                pass
            
            # Configuration 5: Auto detect (most flexible)
            try:
                auto_text = pytesseract.image_to_string(
                    image,
                    config='--psm 3 --oem 3'
                )
                if auto_text.strip() and auto_text not in extracted_texts:
                    extracted_texts.append(auto_text)
            except:
                pass
            
            # Configuration 6: Treat as single word
            try:
                word_text = pytesseract.image_to_string(
                    image,
                    config='--psm 8 --oem 3'
                )
                if word_text.strip() and word_text not in extracted_texts:
                    extracted_texts.append(word_text)
            except:
                pass
            
            # Combine all extracted text from this page
            if extracted_texts:
                page_text = "\n".join(extracted_texts)
                text += f"\n--- Page {i+1} (OCR) ---\n{page_text}\n"
                    
    except Exception as e:
        print(f"Error with OCR processing: {e}")

    return text.strip()

def preprocess_for_math_content(image):
    """Placeholder - not available with old Tesseract"""
    return image

def enhance_contrast_for_handwriting(image):
    """Placeholder - not available with old Tesseract"""
    return image

def compute_similarity(texts):
    """Enhanced similarity computation with modern Tesseract 5.5.2 support"""
    if len(texts) < 2:
        return []

    # Clean and preprocess texts
    processed_texts = []
    for text in texts:
        if text:
            # Remove page separators and normalize
            cleaned = text.replace('--- Page', '').replace('---', '')
            # Remove method labels
            cleaned = cleaned.replace('(Standard)', '').replace('(Alternative)', '').replace('(Modern OCR)', '')
            # Remove extra whitespace and newlines
            cleaned = ' '.join(cleaned.split())
            
            # Remove common English stop words
            stop_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'a', 'an', 'as', 'from', 'into', 'about', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once']
            for stop_word in stop_words:
                cleaned = cleaned.replace(f' {stop_word} ', ' ')
            
            # Remove common Arabic stop words
            arabic_stop_words = ['في', 'من', 'إلى', 'على', 'مع', 'هذا', 'هذه', 'ذلك', 'تلك', 'و', 'ف', 'ب', 'ل', 'ك', 'كان', 'كانت', 'يكون', 'تكون', 'ليس', 'ليست', 'ما', 'ماذا', 'كيف', 'متى', 'أين', 'لماذا', 'كم', 'أي']
            for stop_word in arabic_stop_words:
                cleaned = cleaned.replace(f' {stop_word} ', ' ')
            
            processed_texts.append(cleaned)
        else:
            processed_texts.append("")

    # Use TF-IDF with comprehensive parameters for mixed Arabic/English content
    vectorizer = TfidfVectorizer(
        max_features=20000,  # Increased for better coverage
        ngram_range=(1, 6),  # Include up to 6-grams for pattern matching
        lowercase=False,  # Important for Arabic
        token_pattern=r'(?u)[\w\+\-\×\÷\=\√\∑\∏\∫\∞\≈\≠\≤\≥\π\θ\α\β\γ\δ\λ\μ\σ\φ\ψ\ω\.\,\;\:\!\?\(\)\[\]\{\}ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئابةة]+',
        min_df=1,  # Include all terms
        sublinear_tf=True,
        analyzer='char_wb',  # Character-based for better OCR recognition
        strip_accents='unicode'
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(processed_texts)
        cosine_sim = cosine_similarity(tfidf_matrix)
        
        results = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                similarity = round(cosine_sim[i][j] * 100, 1)
                if similarity > 0.1:  # Very low threshold for sensitive detection
                    results.append({
                        'text1_index': i,
                        'text2_index': j,
                        'similarity': similarity,
                        'text1_preview': processed_texts[i][:300] + "..." if len(processed_texts[i]) > 300 else processed_texts[i],
                        'text2_preview': processed_texts[j][:300] + "..." if len(processed_texts[j]) > 300 else processed_texts[j]
                    })

        # Sort by similarity score
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results
        
    except Exception as e:
        print(f"Error computing similarity: {e}")
        return []
