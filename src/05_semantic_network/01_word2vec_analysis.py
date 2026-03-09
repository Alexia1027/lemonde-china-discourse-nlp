"""
Word2Vec Semantic Distance Analysis
-----------------------------------
Trains a Word2Vec model on the French corpus to map the latent semantic space.
Calculates cosine similarities to uncover subconscious editorial associations 
(e.g., comparing the proximity of 'China', 'Russia', and 'Taiwan' to concepts like 'threat').
"""

import string
import os
from gensim.models import Word2Vec

def load_stopwords(filepath):
    print(f"Loading stopwords from {filepath}...")
    with open(filepath, "r", encoding="utf-8") as file:
        return set(file.read().splitlines())

def train_semantic_model(corpus_path, stopword_path, vector_size=50, window=5, min_count=5, epochs=30):
    """
    Cleans the text line-by-line (preserving context boundaries) and trains a Word2Vec model.
    """
    stop_words = load_stopwords(stopword_path)
    print("✅ Stopwords loaded. Cleaning text and preserving contextual boundaries...")

    cleaned_sentences = []

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        return None

    # Process line by line to preserve sentence/paragraph boundaries for the sliding window
    with open(corpus_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().lower()
            if not line:
                continue
            
            # Remove punctuation
            line = line.translate(str.maketrans('', '', string.punctuation))
            
            # Crucial NLP trick for French: Replace apostrophes with spaces 
            # to split words like "l'état" into "l" and "état"
            line = line.replace("'", " ").replace("’", " ")
            
            # Tokenize and filter
            words = line.split()
            filtered_words = [word for word in words if word not in stop_words]
            
            if filtered_words:
                cleaned_sentences.append(filtered_words)

    print(f"✅ Text cleaning complete. Extracted {len(cleaned_sentences)} valid contextual blocks.")
    print(f"🚀 Igniting Word2Vec engine (Dimensions: {vector_size}, Window: {window})...")

    # Train the Word2Vec model (Using updated Gensim 4.x parameters: vector_size and epochs)
    model = Word2Vec(sentences=cleaned_sentences, vector_size=vector_size, window=window, min_count=min_count, epochs=epochs, workers=4)
    print("🎉 Training complete! Latent semantic space mapped.\n")
    return model

def analyze_discourse_distances(model):
    """
    Executes specific hypothesis tests using Cosine Similarity in the vector space.
    """
    if model is None:
        return

    # --- Test 1: Finding the closest concepts to a target word ---
    target_word = "menace"
    print(f"--- Top 15 closest terms to '{target_word}' ---")
    try:
        similar_words = model.wv.most_similar(target_word, topn=15)
        for word, score in similar_words:
            print(f"  - {word}: {score:.4f}")
    except KeyError:
        print(f"Word '{target_word}' not found in vocabulary.")

    print("\n--- Hypothesis Testing: Who is the 'Threat'? ---")
    # --- Test 2: Comparative proximity to negative framing ---
    entities = ['chine', 'russie', 'taïwan']
    concepts = ['menace', 'offensive']

    for concept in concepts:
        print(f"\n[ Proximity to '{concept}' ]")
        for entity in entities:
            try:
                score = model.wv.similarity(entity, concept)
                print(f"Distance between '{entity}' and '{concept}': {score:.4f}")
            except KeyError as e:
                print(f"Skipping {e} - not in vocab.")

# ==========================================
# Execution Switchboard
# ==========================================
if __name__ == "__main__":
    pass
    # Define paths
    # corpus_file = "../../data/raw/2024_corpus.txt"
    # stopwords_file = "../../resources/stopwords-fr.txt"
    
    # Run Pipeline
    # w2v_model = train_semantic_model(corpus_file, stopwords_file)
    # analyze_discourse_distances(w2v_model)
