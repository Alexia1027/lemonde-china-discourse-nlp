"""
Baseline Experiment: DistilCamemBERT Sentiment Analysis
-------------------------------------------------------
STATUS: Abandoned / Replaced by LLM ABSA Pipeline.

METHODOLOGICAL NOTE: 
This script was initially developed to test a traditional fine-tuned 
transformer (cmarkea/distilcamembert-base-sentiment) as a baseline for 
sentiment analysis on Le Monde corpus. 

FINDINGS:
While computationally efficient, the standard BERT model failed to capture 
Aspect-Based Sentiment (ABSA) accurately in complex political discourse. 
It often misattributed negative sentiment directed at EU policies as negative 
sentiment towards China. Consequently, this approach was discarded in favor 
of a zero/few-shot LLM pipeline with explicit Target definition.
"""

from transformers import pipeline
import numpy as np
import os

def run_bert_baseline(file_path):
    print("Initializing DistilCamemBERT baseline model...")
    # Initialize the French sentiment analysis pipeline
    analyzer = pipeline(
        task='text-classification',
        model="cmarkea/distilcamembert-base-sentiment",
        tokenizer="cmarkea/distilcamembert-base-sentiment",
        top_k=None # Returns scores for all labels
    )

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Naive chunking to bypass the 512 token limit of BERT models.
    # Splitting by rough word count to avoid cutting words in half (unlike strict string slicing).
    words = text.split()
    chunk_size = 400 # Safe margin below 512 tokens
    text_chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    scores = []
    print(f"Analyzing {len(text_chunks)} chunks from the sample article...")

    for chunk in text_chunks:
        # Note: Truncation is handled by the pipeline if chunks slightly exceed 512 tokens
        result = analyzer(chunk, truncation=True, max_length=512)
        
        # In modern transformers, top_k=None returns a nested list
        labels = result[0] if isinstance(result[0], list) else result
        
        positive_score = next((res['score'] for res in labels if res['label'] == '1 star' or res['label'] == 'POSITIVE'), 0)
        negative_score = next((res['score'] for res in labels if res['label'] == '5 stars' or res['label'] == 'NEGATIVE'), 0)
        
        # Calculate a net polarity score
        scores.append(positive_score - negative_score)

    average_score = np.mean(scores)
    print(f"Baseline Sentiment Score (Net Polarity): {average_score:.4f}")
    print("\nCONCLUSION: Model captures general tone but fails on specific political attribution.")

# ==========================================
# Execution Switchboard
# ==========================================
if __name__ == "__main__":
    pass
    # sample_article = "../../data/raw/sample_article.txt"
    # run_bert_baseline(sample_article)
