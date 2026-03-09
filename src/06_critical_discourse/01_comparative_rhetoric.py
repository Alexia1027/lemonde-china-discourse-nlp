"""
Comparative Rhetoric & "Othering" Analysis Module
-------------------------------------------------
This script operationalizes the sociological concept of "The Other" (l'Altérité).
It uses rule-based NLP to extract sentences where the "Self" (Europe/France) 
and the "Other" (China) are explicitly contrasted using comparative or 
adversarial markers (e.g., 'tandis que', 'au contraire').
"""

import os
import re

def analyze_comparative_rhetoric(input_file_path, output_report_path):
    """
    Scans a corpus for comparative rhetoric by matching sentences containing 
    Target A (China), Target B (Europe/France), and explicit contrast markers.
    """
    # 1. Define Lexicons (French)
    china_terms = {'chine', 'chinois', 'pékin', 'beijing', 'rpc'}
    europe_terms = {'france', 'français', 'europe', 'européen', 'ue', 'paris', 'bruxelles', 'occident'}
    
    # Rhetorical markers for contrast and comparison
    contrast_markers = {
        'alors que', 'tandis que', 'en revanche', 'par contre', 'contrairement', 
        'au contraire', 'par rapport à', 'comparé', 'différence', 'plus que', 
        'moins que', "à l'inverse", 'toutefois', 'néanmoins', 'cependant',
        'autrement', 'distinction', 'similairement', 'de même que'
    }

    if not os.path.exists(input_file_path):
        print(f"Error: Input file not found at {input_file_path}")
        return

    with open(input_file_path, 'r', encoding='utf-8') as f:
        articles = [art.strip() for art in f.read().split('###') if art.strip()]

    results = []
    print(f"Scanning {len(articles)} articles for comparative rhetoric...")

    for art in articles:
        lines = art.split('\n')
        title = lines[0].strip() if lines else "Untitled"
        
        # Split article into sentences (regex handles French punctuation . ! ?)
        sentences = re.split(r'(?<=[.!?])\s+', art.replace('\n', ' '))
        match_details = []
        
        for sentence in sentences:
            sent_lower = sentence.lower()
            
            # Boolean checks for the presence of specific discourse elements
            has_china = any(w in sent_lower for w in china_terms)
            has_europe = any(w in sent_lower for w in europe_terms)
            has_contrast = any(c in sent_lower for c in contrast_markers)
            
            # Evaluation Criteria:
            # 1. Contains A, B, and a contrast marker OR
            # 2. Contains A, B, and a comparative degree (plus/moins)
            if (has_china and has_europe and has_contrast) or \
               (has_china and has_europe and (' plus ' in sent_lower or ' moins ' in sent_lower)):
                match_details.append(sentence.strip())

        if match_details:
            results.append({
                'title': title,
                'count': len(match_details),
                'snippets': match_details
            })

    # 2. Export Qualitative Report
    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    with open(output_report_path, 'w', encoding='utf-8') as f:
        f.write("=== Comparative Rhetoric & 'Othering' Discourse Report ===\n")
        f.write(f"Total articles scanned: {len(articles)}\n")
        f.write(f"Articles exhibiting contrastive rhetoric: {len(results)}\n\n")
        
        # Sort by intensity (number of comparative sentences)
        results.sort(key=lambda x: x['count'], reverse=True)
        
        for res in results:
            f.write(f"[Article Title]: {res['title']}\n")
            f.write(f"[Comparative Sentences Count]: {res['count']}\n")
            f.write(f"[Extracted Snippets]:\n")
            for i, snippet in enumerate(res['snippets']):
                f.write(f"  ({i+1}) {snippet}\n")
            f.write("-" * 50 + "\n\n")

    print(f"Analysis complete! Qualitative report saved to: {output_report_path}")

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    pass
    # source_path = "../../data/processed/subset_corpus.txt"
    # report_path = "../../data/output/comparative_rhetoric_report.txt"
    # analyze_comparative_rhetoric(source_path, report_path)
