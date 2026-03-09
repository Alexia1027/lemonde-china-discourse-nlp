"""
Discourse Cartography Visualization Module
------------------------------------------
Generates a high-resolution bubble chart mapping the broadness (number of articles)
vs. intensity (total frequency) of key terms in the Le Monde corpus.
Utilizes `adjustText` to prevent label overlapping for publication-quality output.
"""

import matplotlib.pyplot as plt
import pandas as pd
from adjustText import adjust_text
import os

def plot_discourse_cartography(output_path):
    """
    Generates and saves a quadrant bubble chart based on term frequencies.
    """
    print("Initializing data for discourse cartography...")
    
    # 1. Raw data input (Merged 'Chine' and 'Pékin')
    raw_data = {
        'term': [
            'Xi Jinping', 'Investissement', 'Exportation', 'Taïwan', 'Croissance', 
            'Parti communiste', 'Subvention', 'Batterie', 'Sécurité nationale', 
            'Immobilier', 'Ralentissement', 'Empire du milieu', 'Surveillance', 
            'Routes de la soie', 'Répression', 'Dette', 'PCC', 'Chômage', 
            'Propagande', 'Mer de Chine', 'Surcapacité', 'Découplage', 'Censure', 
            'Ingérence', 'Jeunesse', 'Espionnage', 'Coercition', 'Dissident', 
            'Déflation', 'Dumping', 'Soft power', 'Véhicule électrique'
        ],
        'articles': [
            752, 531, 489, 443, 357, 369, 264, 246, 245, 193, 183, 159, 119, 
            130, 120, 107, 107, 95, 103, 104, 92, 84, 73, 70, 60, 56, 57, 47, 
            42, 35, 37, 27
        ],
        'frequency': [
            4814, 2246, 2886, 5630, 1486, 1083, 1016, 1178, 892, 600, 536, 408, 417, 
            530, 445, 547, 526, 212, 344, 628, 419, 340, 200, 237, 200, 255, 205, 186, 
            124, 167, 124, 74
        ],
        'category': [
            'Politique', 'Économie', 'Économie', 'Politique', 'Économie', 
            'Politique', 'Économie', 'Économie', 'Politique', 
            'Économie', 'Économie', 'Société', 'Société', 
            'Économie', 'Politique', 'Économie', 'Politique', 'Société', 
            'Politique', 'Politique', 'Économie', 'Économie', 'Politique', 
            'Politique', 'Société', 'Politique', 'Politique', 'Politique', 
            'Économie', 'Économie', 'Société', 'Économie'
        ]
    }

    df = pd.DataFrame(raw_data)

    # 2. Plot styling configuration
    plt.rcParams['font.sans-serif'] = ['Arial'] # Standard font for academic papers
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

    # Color mapping for different categories
    colors = {'Politique': '#1f77b4', 'Économie': '#ff7f0e', 'Société': '#2ca02c'}

    # 3. Draw scatter plot (Bubble size corresponds to frequency)
    print("Rendering scatter points...")
    for cat in colors:
        sub_df = df[df['category'] == cat]
        ax.scatter(sub_df['articles'], sub_df['frequency'], 
                   c=colors[cat], s=sub_df['frequency']/5, 
                   label=cat, alpha=0.6, edgecolors='white')

    # 4. Add labels and auto-adjust positions to prevent overlap
    print("Applying repel algorithm for text labels (adjustText)...")
    texts = []
    for i, txt in enumerate(df['term']):
        texts.append(ax.text(df['articles'][i], df['frequency'][i], txt, fontsize=9))

    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

    # 5. Draw quadrant lines based on the mean
    ax.axvline(df['articles'].mean(), color='gray', linestyle='--', lw=1, alpha=0.5)
    ax.axhline(df['frequency'].mean(), color='gray', linestyle='--', lw=1, alpha=0.5)

    # 6. Chart decorations (Kept in French to match the research context)
    ax.set_title('Cartographie du discours médiatique français sur la Chine (2023-2025)', fontsize=16, pad=20)
    ax.set_xlabel('Largeur du discours : Nombre d\'articles (Broadness)', fontsize=12)
    ax.set_ylabel('Intensité du discours : Fréquence totale (Intensity)', fontsize=12)

    # Add quadrant explanatory text
    ax.text(df['articles'].max()*0.8, df['frequency'].max()*0.95, 'Sujets Dominants', color='gray', fontsize=10, fontweight='bold')
    ax.text(df['articles'].min(), df['frequency'].max()*0.95, 'Sujets de Niche / Intenses', color='gray', fontsize=10, fontweight='bold')

    ax.legend(title="Catégories", loc='lower right')
    ax.grid(True, linestyle=':', alpha=0.4)

    # 7. Save and display
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"High-resolution chart successfully generated and saved to: {output_path}")

# ==========================================
# Execution
# ==========================================
if __name__ == "__main__":
    output_filepath = "../../data/output/Analyse_Chine_Visualisation.png"
    plot_discourse_cartography(output_filepath)
