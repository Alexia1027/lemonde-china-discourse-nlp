"""
Text Cleaning Module for French Corpus
--------------------------------------
This module provides functions to clean raw French text by lowercasing, 
removing punctuation, and filtering out custom stopwords. 
It is designed to be imported and used dynamically in downstream NLP tasks 
(like LDA or Word2Vec) to keep raw data immutable.
"""

import string
import os

def load_stopwords(filepath):
    """
    Loads a custom stopword list from a text file.
    
    Args:
        filepath (str): Path to the stopwords .txt file.
    Returns:
        set: A set of stopwords for O(1) lookup.
    """
    print(f"Loading custom stopwords from: {filepath}")
    if not os.path.exists(filepath):
        print(f"Warning: Stopwords file not found at {filepath}")
        return set()
        
    with open(filepath, "r", encoding="utf-8") as file:
        # Read stopwords and remove newline characters
        return set(file.read().splitlines())

def clean_french_text(text, stop_words):
    """
    Cleans the input text by:
    1. Converting to lowercase
    2. Removing all punctuation
    3. Tokenizing (splitting by space)
    4. Removing stopwords
    
    Args:
        text (str): The raw text to be cleaned.
        stop_words (set): The set of stopwords to filter out.
    Returns:
        str: The cleaned text as a single string.
    """
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove punctuation using translation table
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Tokenize
    words = text.split()
    
    # 4. Remove stopwords
    words = [word for word in words if word not in stop_words]
    
    return " ".join(words)

# ==========================================
# Example Usage (Can be run directly or imported)
# ==========================================
if __name__ == "__main__":
    # Define relative paths
    stopwords_path = "../../resources/stopwords-fr.txt"
    raw_text_path = "../../data/raw/2024_corpus.txt"
    cleaned_output_path = "../../data/processed/2024_cleaned.txt"
    
    # Run the pipeline (commented out for safety)
    """
    # Load resources
    custom_stopwords = load_stopwords(stopwords_path)
    
    # Read raw text
    with open(raw_text_path, "r", encoding="utf-8") as file:
        raw_text = file.read()
        
    # Clean text
    print("Cleaning text...")
    cleaned_text = clean_french_text(raw_text, custom_stopwords)
    
    # Save cleaned text
    os.makedirs(os.path.dirname(cleaned_output_path), exist_ok=True)
    with open(cleaned_output_path, "w", encoding="utf-8") as file:
        file.write(cleaned_text)
    
    print(f"Text cleaning complete. Saved to {cleaned_output_path}")
    """
