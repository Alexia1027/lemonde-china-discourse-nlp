# lemonde-china-discourse-nlp
Computational text analysis of Le Monde's coverage on China (2023-2025) using LLM and NLP pipelines.
# 📰 Decoding Le Monde: A Computational Discourse Analysis of China (2023-2025)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![NLP](https://img.shields.io/badge/NLP-Spacy%20%7C%20Gensim-green.svg)]()
[![Method](https://img.shields.io/badge/Methodology-Mixed--Methods-orange.svg)]()

## 📌 Overview
This repository contains the computational pipeline for analyzing the French center-left media's (*Le Monde*) discourse construction of China from 2023 to 2025. 

Combining **Large Language Models (LLMs)**, **unsupervised machine learning (LDA/Word2Vec)**, and **Critical Discourse Analysis (CDA)**, this project examines narratives across geopolitics, economic supply chains, and social issues. It also includes an analysis of audience reception via YouTube comments.

## 🔬 Methodological Pipeline (Human-in-the-Loop)

This project employs a mixed-methods approach:

1. **Data Preparation:** Scripts to parse, split, and clean raw docx/txt files curated from *Le Monde* archives, preserving contextual boundaries for analysis.
2. **LLM-Assisted Coding (Zero-Shot ABSA & Framing):** Utilizes Gemini Pro via batch-prompting for aspect-based sentiment and framing analysis. Prompts are designed to map Entman's framing theory to operationalized codes, incorporating context-reset mechanisms. *(Note: Traditional BERT models were evaluated as baselines but struggled with target-misalignment; see baseline experiments).*
3. **Semantic Mapping & Co-occurrence:** Dictionary-based matching and Word2Vec models to measure the semantic distance between entities (e.g., *China*, *Russia*) and specific concepts (e.g., *Menace*).
4. **Topic Modeling:** Boolean retrieval for isolating sub-corpuses (e.g., Taiwan/SCS issues) followed by unsupervised LDA clustering to identify sub-narratives.
5. **Audience Reception Clustering:** Scraping YouTube news comments and applying K-Means clustering on one-hot encoded LLM annotations to categorize audience stances.

## 🗂️ Repository Structure

```text
├── prompts/                         # Engineering-grade Codebooks for LLM (Framing, ABSA)
├── resources/                       # Custom French stopwords and rhetorical lexicons
├── src/
│   ├── 01_data_preparation/         # Corpus subsetting, docx/txt splitting, and merging
│   ├── 02_nlp_analysis/             # Tokenization, lemmatization, and document/window-level co-occurrence
│   ├── 03_visualization/            # Publication-quality discourse cartography (adjustText bubble charts)
│   ├── 04_topic_modeling/           # Unsupervised LDA (Gensim/pyLDAvis) & boolean retrieval pipelines
│   ├── 05_semantic_network/         # Word2Vec training and Cosine Similarity hypothesis testing
│   ├── 06_critical_discourse/       # Rule-based NLP for Comparative Rhetoric and "Othering" extraction
│   ├── 07_audience_reception/       # YouTube scraping and K-Means Persona Clustering
│   └── 08_experiments_and_baselines/# Abandoned baselines (e.g., DistilCamemBERT evaluation)
```

## 📊 Key Analytical Features
Discourse Cartography: Bubble charts mapping the document frequency vs. total frequency of keywords.
Semantic Prosody (Word2Vec): Preserves sentence boundaries to calculate cosine similarities between geopolitical actors and selected terms.
Rule-based CDA: Extracts explicit "Othering" by identifying comparative markers (tandis que, au contraire) juxtaposing Europe and China.

## 🚀 How to Replicate
Clone the repository
Install dependencies: pip install -r requirements.txt
Download the French Spacy model: python -m spacy download fr_core_news_sm
Note: **Raw copyrighted texts from Le Monde are not included in this public repository to respect intellectual property.** Ensure your dataset is placed in a local data/raw/ directory before running the scripts in numerical order.

Contact: alexia1027@outlook.com
