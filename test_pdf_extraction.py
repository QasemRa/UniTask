#!/usr/bin/env python
"""
Test script to verify PDF text extraction works
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from myapp.utils import extract_text_from_pdf, compute_similarity

def test_extraction():
    """Test the enhanced PDF extraction"""
    print("Testing enhanced PDF text extraction...")
    
    # Test with sample texts
    sample_texts = [
        "This is a test document about machine learning and artificial intelligence. Machine learning is a subset of AI that focuses on algorithms.",
        "Artificial intelligence and machine learning are transforming technology. AI encompasses various technologies including machine learning algorithms."
    ]
    
    # Test similarity computation
    similarities = compute_similarity(sample_texts)
    
    print(f"Found {len(similarities)} similarities:")
    for sim in similarities:
        print(f"Similarity: {sim['similarity']}%")
        print(f"Text 1: {sim['text1_preview']}")
        print(f"Text 2: {sim['text2_preview']}")
        print("-" * 50)

if __name__ == "__main__":
    test_extraction()
