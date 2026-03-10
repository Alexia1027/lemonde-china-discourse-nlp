# lemonde-china-discourse-nlp
Computational text analysis of Le Monde's coverage on China (2023-2025) using LLM and NLP pipelines.
# 📰 Decoding Le Monde: A Computational Discourse Analysis of China (2023-2025)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![NLP](https://img.shields.io/badge/NLP-Spacy%20%7C%20Gensim-green.svg)]()
[![Method](https://img.shields.io/badge/Methodology-Mixed--Methods-orange.svg)]()

## 📌 Overview
This repository contains the complete computational pipeline for analyzing the French center-left media's (*Le Monde*) discourse construction of China from 2023 to 2025. 

Combining **Large Language Models (LLMs)**, **unsupervised machine learning (LDA/Word2Vec)**, and **Critical Discourse Analysis (CDA)**, this project maps the complex narrative topology bridging geopolitics, economic supply chains, and social ideology. It also closes the communication loop by analyzing audience reception via YouTube comments.

## 🔬 Methodological Pipeline (Human-in-the-Loop)

Unlike standard "black-box" text mining, this project employs a highly granular, mixed-methods approach:

1. **Rigorous Data Wrangling:** Custom scripts to parse, split, and clean raw docx/txt files curated from *Le Monde*'s paywalled archives, ensuring high-fidelity contextual boundaries.
2. **LLM-Assisted Qualitative Coding (Zero-Shot ABSA & Framing):** - Instead of relying on traditional BERT models (which struggle with target-misalignment in complex political rhetoric—*see baseline experiments*), this project utilizes **Gemini Pro** via rigorous batch-prompting. 
   - Prompts strictly control context windows (10-20k tokens per batch) with context-reset mechanisms to prevent hallucination and autoregressive pollution, strictly mapping Entman's framing theory to operationalized codes.
3. **Semantic Mapping & Co-occurrence:** Custom dictionary-based matching and Word2Vec models to measure the latent semantic distance between entities (e.g., *China*, *Russia*) and normative concepts (e.g., *Menace*, *Offensive*).
4. **Drill-down Topic Modeling:** Boolean retrieval sets isolating micro-corpuses (e.g., Taiwan/SCS crises) for unsupervised LDA clustering, uncovering latent sub-narratives.
5. **Audience Reception Clustering:** Scraping YouTube news comments and applying K-Means clustering on one-hot encoded LLM annotations to automatically derive Audience Personas (e.g., Pragmatic Consumer vs. Political Reflective).

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

📊 Key Analytical Features
Discourse Cartography: High-resolution quadrant bubble charts mapping the "Broadness" vs. "Intensity" of agenda-setting keywords.
Semantic Prosody (Word2Vec): Preserves sentence boundaries to map precise cosine similarities between geopolitical actors.
Rule-based CDA: Extracts explicit "Othering" by identifying comparative markers (tandis que, au contraire) juxtaposing Europe and China.

🚀 How to Replicate
Clone the repository: git clone https://github.com/[Your-Username]/[Your-Repo-Name].git
Install dependencies: pip install -r requirements.txt
Download the French Spacy model: python -m spacy download fr_core_news_sm
Note: **Raw copyrighted texts from Le Monde are not included in this public repository to respect intellectual property.** Ensure your dataset is placed in a local data/raw/ directory before running the scripts in numerical order.

Contact: alexia1027@outlook.com
