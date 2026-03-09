"""
Topic Modeling & Micro-Corpus Extraction Pipeline
-------------------------------------------------
This pipeline executes a deep-dive analysis on a specific sub-corpus (e.g., Taiwan-related articles).
It includes:
1. Unsupervised Topic Modeling (LDA via Gensim & pyLDAvis).
2. Thematic Visualization (Barplot matrix via Seaborn).
3. Precision Boolean Retrieval (Extracting specific micro-corpuses based on LDA findings).
"""

import os
import re
import spacy
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ==========================================
# 1. Unsupervised LDA Topic Modeling
# ==========================================
def train_lda_model(input_file, stopword_file, output_html, num_topics=10):
    """
    Trains an LDA model on the target corpus and generates an interactive HTML visualization.
    """
    print("Loading French NLP model and stopwords...")
    try:
        nlp = spacy.load("fr_core_news_sm", disable=['ner', 'parser'])
    except OSError:
        print("Spacy model 'fr_core_news_sm' not found. Please install it using: python -m spacy download fr_core_news_sm")
        return

    with open(stopword_file, 'r', encoding='utf-8') as f:
        custom_stopwords = set([line.strip().lower() for line in f if line.strip()])

    print(f"Reading corpus: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_articles = re.split(r'###', f.read())
    
    # Filter short noise
    articles = [a.strip() for a in raw_articles if len(a.strip()) > 100]
    print(f"Valid articles for LDA: {len(articles)}")

    def preprocess(text):
        doc = nlp(text.lower())
        tokens = []
        for token in doc:
            # Filter criteria: Alpha, length > 2, not stopword, specific POS tags
            if (token.is_alpha and len(token.text) > 2 
                and token.text not in custom_stopwords 
                and not token.is_stop
                and token.pos_ in ['NOUN', 'ADJ', 'PROPN']):
                tokens.append(token.lemma_)
        return tokens

    print("Tokenizing and lemmatizing (this may take a while)...")
    processed_docs = [preprocess(art) for art in articles]

    # Build Dictionary and Corpus
    dictionary = corpora.Dictionary(processed_docs)
    dictionary.filter_extremes(no_below=2, no_above=0.6)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    print(f"Training LDA model ({num_topics} topics)...")
    lda_model = LdaModel(
        corpus=corpus, id2word=dictionary, num_topics=num_topics, 
        passes=20, iterations=100, random_state=42, alpha='auto'
    )

    print("\n--- Top Keywords per Topic ---")
    for idx, topic in lda_model.print_topics(num_topics=num_topics, num_words=10):
        print(f"Topic {idx}: {topic}")

    print(f"\nGenerating interactive visualization: {output_html}")
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, output_html)
    print("LDA Analysis Complete!")


# ==========================================
# 2. Thematic Distribution Visualization
# ==========================================
def plot_lda_themes(output_image_path):
    """
    Visualizes the top words for human-categorized LDA topics using a Seaborn barplot matrix.
    """
    print("Rendering LDA thematic distribution matrix...")
    
    # Raw data derived from the Gensim model output
    raw_data = {
        "Topic 0": {"militaire": 0.018, "armée": 0.012, "défense": 0.010, "île": 0.009, "taïwanais": 0.009, "zone": 0.007, "nucléaire": 0.006, "missile": 0.006, "philippine": 0.005, "navire": 0.005},
        "Topic 6": {"japon": 0.020, "sud": 0.011, "asie": 0.011, "région": 0.010, "corée": 0.009, "pacifique": 0.009, "ministre": 0.009, "philippine": 0.007, "archipel": 0.007, "alliance": 0.007},
        "Topic 1": {"entreprise": 0.012, "européen": 0.010, "mondial": 0.010, "marché": 0.008, "production": 0.008, "milliard": 0.008, "économique": 0.007, "commercial": 0.006, "puce": 0.006, "europe": 0.006},
        "Topic 8": {"trump": 0.011, "donald": 0.007, "droit": 0.007, "nvidia": 0.005, "entreprise": 0.005, "puce": 0.005, "usine": 0.005, "nouveau": 0.005, "puissance": 0.005, "commercial": 0.004},
        "Topic 3": {"taïwanais": 0.018, "parti": 0.012, "européen": 0.009, "île": 0.008, "militaire": 0.006, "ching": 0.006, "relation": 0.006, "dpp": 0.006, "kmt": 0.006, "ministre": 0.006},
        "Topic 7": {"france": 0.009, "taïwanais": 0.007, "africain": 0.006, "afrique": 0.006, "panama": 0.005, "relation": 0.005, "gouvernement": 0.005, "pari": 0.005, "nouveau": 0.005, "port": 0.005},
        "Topic 9": {"trump": 0.017, "donald": 0.011, "russie": 0.009, "relation": 0.009, "ukraine": 0.009, "jinping": 0.008, "washington": 0.007, "sécurité": 0.005, "affaire": 0.005, "question": 0.005},
        "Topic 5": {"article": 0.007, "international": 0.006, "hongkong": 0.006, "droit": 0.005, "dollar": 0.005, "autorité": 0.005, "yuan": 0.005, "économique": 0.004, "relation": 0.004, "parti": 0.004},
    }

    # Meta-dimensions assigned via human interpretation
    dimensions = {
        "Topic 0": "D1: Geopolitics & Military", "Topic 6": "D1: Geopolitics & Military",
        "Topic 1": "D2: Tech & Supply Chain", "Topic 8": "D2: Tech & Supply Chain",
        "Topic 3": "D3: Taiwan Politics", "Topic 7": "D3: Taiwan Politics",
        "Topic 9": "D4: Great Power Game", "Topic 5": "D4: Great Power Game"
    }

    sns.set_theme(style="whitegrid")
    plt.rcParams['font.sans-serif'] = ['Arial']
    fig, axes = plt.subplots(2, 4, figsize=(20, 10), sharex=False)
    axes = axes.flatten()

    colors = ["#4C72B0", "#4C72B0", "#55A868", "#55A868", "#C44E52", "#C44E52", "#8172B3", "#8172B3"]

    for i, (topic_name, words_dict) in enumerate(raw_data.items()):
        df = pd.DataFrame(list(words_dict.items()), columns=['Word', 'Weight']).sort_values(by='Weight', ascending=False)
        sns.barplot(x='Weight', y='Word', data=df, ax=axes[i], color=colors[i], alpha=0.8)
        
        axes[i].set_title(f"{topic_name}\n{dimensions[topic_name]}", fontsize=12, fontweight='bold')
        axes[i].set_xlabel("Weight", fontsize=10)
        axes[i].set_ylabel("")
        axes[i].tick_params(labelsize=10)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle('LDA Topic Distribution by Analytical Dimensions', fontsize=18, fontweight='bold')
    
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_image_path}")


# ==========================================
# 3. Precision Boolean Retrieval (Sub-setting)
# ==========================================
def extract_precise_micro_corpuses(input_file, output_dir):
    """
    Uses exact boolean set operations (issubset) to extract highly specific micro-corpuses 
    based on the findings from the LDA model (e.g., intersection of Taiwan, Philippines, and Ships).
    """
    print(f"\nExecuting precision retrieval on: {input_file}")
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        articles = [art.strip() for art in f.read().split('###') if art.strip()]

    micro_corpus_1 = []
    micro_corpus_2 = []

    for art in articles:
        # Extract alphanumeric words and convert to a mathematical set
        words = set(re.findall(r'\w+', art.lower()))

        # Logic 1: ALL keywords must be present
        if {"philippine", "navire", "taïwan"}.issubset(words):
            micro_corpus_1.append(art)

        # Logic 2: ALL keywords must be present
        if {"ukraine", "taïwan"}.issubset(words):
            micro_corpus_2.append(art)

    def save_corpus(filename, data):
        path = os.path.join(output_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n\n###\n\n".join(data))
        return len(data)

    count1 = save_corpus("MicroCorpus_SCS_Conflict_Precise.txt", micro_corpus_1)
    count2 = save_corpus("MicroCorpus_Ukraine_Taiwan_Precise.txt", micro_corpus_2)

    print("\n--- Boolean Retrieval Report ---")
    print(f"Total articles scanned: {len(articles)}")
    print(f"Micro-Corpus 1 (Philippine AND Navire AND Taïwan) hits: {count1}")
    print(f"Micro-Corpus 2 (Ukraine AND Taïwan) hits: {count2}")
    print(f"Extracted corpuses saved to: {output_dir}")

# ==========================================
# Execution Switchboard
# ==========================================
if __name__ == "__main__":
    pass
    # Define Paths
    # corpus_path = "../../data/processed/Taiwan_related_articles.txt"
    # stopword_path = "../../resources/stopwords-fr.txt"
    # lda_html_out = "../../data/output/Taiwan_LDA_10Topics.html"
    # lda_png_out = "../../data/output/LDA_Dimensions_Matrix.png"
    # subset_out_dir = "../../data/processed/micro_corpuses/"

    # --- Run Pipeline Steps ---
    # 1. train_lda_model(corpus_path, stopword_path, lda_html_out)
    # 2. plot_lda_themes(lda_png_out)
    # 3. extract_precise_micro_corpuses(corpus_path, subset_out_dir)
