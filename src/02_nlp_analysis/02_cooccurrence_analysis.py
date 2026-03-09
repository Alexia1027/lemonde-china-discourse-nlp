"""
Co-occurrence Analysis Module
-----------------------------
This script performs two types of co-occurrence analysis based on a custom 
dictionary of politically, economically, and socially significant terms:
1. Document-level Co-occurrence: Checks if target terms appear in the same article as core entities (e.g., China, Beijing).
2. Window-level Co-occurrence: Scans a specified word window around core entities to capture immediate semantic prosody.
"""

import re
import pandas as pd
import os

# --- 1. Global Configuration & Custom Dictionary ---

# The core entities we are tracking
CORE_KEYWORDS = ["chine", "pékin"]

# Custom dictionary extracted based on the specific discourse of Le Monde
# Terms are in their base form (roots) to allow for plural matching
CUSTOM_DICT = {
    "Politics": [
        "parti communiste", "pcc", "état-parti", "xi jinping", "répression", 
        "censure", "sécurité nationale", "autoritarisme", "taïwan", "mer de chine",
        "coercition", "loups guerriers", "ingérence", "rival systémique", "propagande",
        "droits de l'homme", "dissident", "espionnage", "loi sur la sécurité"
    ],
    "Economy": [
        "subvention", "surcapacité", "dumping", "prix cassé", "véhicule électrique",
        "batterie", "immobilier", "déflation", "ralentissement", "dette", 
        "routes de la soie", "dérisquage", "découplage", "concurrence déloyale",
        "omc", "croissance", "investissement", "exportation"
    ],
    "Society_Culture": [
        "996", "involution", "neijuan", "chômage", "vieillissement",
        "hukou", "prospérité commune", "surveillance", "reconnaissance faciale",
        "empire du milieu", "sinisation", "soft power", "jeunesse", "opinion publique"
    ]
}

# Flatten the dictionary for searching
ALL_DICT_TERMS = [term for sublist in CUSTOM_DICT.values() for term in sublist]

# --- 2. Analytical Functions ---

def document_level_cooccurrence(file_path, output_dir):
    """
    Calculates the document-level co-occurrence between core keywords and dictionary terms.
    """
    print(f"\n--- Starting Document-Level Analysis ---")
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        full_content = f.read()

    articles = re.split(r'###', full_content)
    print(f"Detected {len(articles)} articles.")

    results = []

    for idx, art in enumerate(articles):
        if not art.strip():
            continue
        art_lower = art.lower()
        
        # Check if the article contains core keywords (exact word match)
        found_core = [kw for kw in CORE_KEYWORDS if re.search(rf'\b{kw}\b', art_lower)]
        
        if found_core:
            for term in ALL_DICT_TERMS:
                # Match root + optional plural suffix (s/es)
                pattern = rf'\b{re.escape(term)}(s|es)?\b'
                if re.search(pattern, art_lower):
                    for core_word in found_core:
                        results.append({
                            "Article_ID": idx,
                            "Core_Entity": core_word,
                            "Co_occurring_Term": term
                        })

    df_results = pd.DataFrame(results)

    if not df_results.empty:
        # Group and count
        summary = df_results.groupby(['Core_Entity', 'Co_occurring_Term']).size().reset_index(name='Document_Frequency')
        summary = summary.sort_values(by='Document_Frequency', ascending=False)
        
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "doc_level_cooccurrence.xlsx")
        summary.to_excel(output_file, index=False)
        print(f"Document-level analysis complete. Saved to: {output_file}")
        print(summary.head(10))
    else:
        print("No co-occurrences found.")


def window_level_cooccurrence(file_path, output_dir, window_size=200):
    """
    Calculates the window-level co-occurrence. 
    Note on window_size: Given the stylistic tendency in French journalism to avoid 
    repetition by using pronouns or alternative designations for 'China', a relatively 
    large window size (e.g., 200 words) is recommended to capture the semantic prosody accurately.
    """
    print(f"\n--- Starting Window-Level Analysis (Window Size: {window_size} words) ---")
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()

    # Simple French tokenization: keeps words with hyphens and apostrophes
    tokens = re.findall(r"\b\w+(?:[-\']\w+)*\b", text)
    results = []

    for i, token in enumerate(tokens):
        if token in CORE_KEYWORDS:
            # Define window boundaries
            start = max(0, i - window_size)
            end = min(len(tokens), i + window_size + 1)
            window_content = " ".join(tokens[start:end])
            
            for term in ALL_DICT_TERMS:
                pattern = rf'\b{re.escape(term)}(s|es)?\b'
                matches = re.findall(pattern, window_content)
                
                # If the term appears multiple times in the window, count each instance
                for _ in range(len(matches)): 
                    results.append({
                        "Core_Entity": token,
                        "Co_occurring_Term": term
                    })

    df_results = pd.DataFrame(results)

    if not df_results.empty:
        summary = df_results.groupby(['Core_Entity', 'Co_occurring_Term']).size().reset_index(name='Window_Frequency')
        summary = summary.sort_values(by='Window_Frequency', ascending=False)
        
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"window_level_cooccurrence_ws{window_size}.xlsx")
        summary.to_excel(output_file, index=False)
        print(f"Window-level analysis complete. Saved to: {output_file}")
        print(summary.head(10))
    else:
        print("No co-occurrences found in windows.")

# ==========================================
# Example Usage 
# ==========================================
if __name__ == "__main__":
    pass
    # Define paths
    # input_corpus = "../../data/raw/2023-2025_corpus.txt"
    # output_directory = "../../data/output/"
    
    # Run analysis
    # document_level_cooccurrence(input_corpus, output_directory)
    # window_level_cooccurrence(input_corpus, output_directory, window_size=200)
