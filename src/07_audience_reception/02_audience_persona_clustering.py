"""
Audience Persona Clustering (K-Means)
-------------------------------------
Transforms categorical LLM output (Sentiment, Target, Stance) into one-hot 
encoded features and applies K-Means clustering to automatically discover 
latent audience personas (e.g., The Pragmatic Consumer, The Anti-EU Critic).
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def cluster_audience_personas(csv_path, num_clusters=3):
    """
    Performs KMeans clustering on LLM-annotated YouTube comments.
    """
    print(f"Loading annotated audience data from {csv_path}...")
    # Mock data generation for demonstration (simulating the LLM output)
    # In reality, this reads your processed CSV.
    df = pd.DataFrame({
        'Polarity': [-1, 1, -1, -1, 1, 0, -1, 1],
        'Target': ['EU/French Govt', 'China/Tech', 'China/Tech', 'EU/French Govt', 'China/Tech', 'Consumer', 'Media', 'China/Tech'],
        'Persona_Stance': ['Political Reflective', 'Pragmatic Economic', 'Ideological', 'Political Reflective', 'Pragmatic Economic', 'Pragmatic Economic', 'Troll', 'Pragmatic Economic']
    })
    
    # 1. Feature Engineering: One-Hot Encoding for categorical variables
    print("Applying One-Hot Encoding to categorical features...")
    categorical_cols = ['Target', 'Persona_Stance']
    df_encoded = pd.get_dummies(df, columns=categorical_cols)
    
    # 2. KMeans Clustering
    print(f"Running K-Means algorithm (k={num_clusters})...")
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(df_encoded)
    
    # 3. Analyze Clusters
    print("\n--- Identified Audience Personas (Cluster Profiles) ---")
    for cluster_id in range(num_clusters):
        cluster_data = df[df['Cluster'] == cluster_id]
        print(f"\n[ Persona {cluster_id + 1} ] - Size: {len(cluster_data)} comments")
        print("Dominant Targets:", cluster_data['Target'].mode().tolist())
        print("Dominant Stance:", cluster_data['Persona_Stance'].mode().tolist())
        print("Average Polarity:", cluster_data['Polarity'].mean())

    return df, df_encoded, kmeans

# ==========================================
# Execution Switchboard
# ==========================================
if __name__ == "__main__":
    pass
    # file_path = "../../data/processed/youtube_annotated.csv"
    # df_clustered, encoded_features, km_model = cluster_audience_personas(file_path, num_clusters=3)
