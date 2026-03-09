import re
import os

# 1. Path Configuration (using relative paths for GitHub portability)
# Assuming your code is in the src/ directory and data in the root data/ directory
input_file_path = "../data/raw/corpus.txt"
output_file_path = "../data/processed/key_word_related_articles.txt"

# Define the target keyword for extraction. key_word is just an example and can be replaced.
target_keyword = "key_word"

def extract_articles():
    # 2. Read and Split Articles
    print(f"Reading corpus from: {input_file_path}")
    if not os.path.exists(input_file_path):
        print("Error: Input file not found. Please check the data/raw/ directory.")
        return

    with open(input_file_path, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # Split articles using the '###' delimiter
    articles = re.split(r'###', full_content)
    print(f"Detected a total of {len(articles)} articles.")

    # 3. Filter Articles Containing the Keyword
    selected_articles = []
    print(f"Filtering articles containing the keyword '{target_keyword}'...")

    for art in articles:
        # Skip empty strings
        if not art.strip():
            continue
        
        # Convert to lowercase for robust matching (covers "key_word" and "possible_variations_of_keywords")
        art_lower = art.lower()
        if target_keyword.lower() in art_lower or "taiwan" in art_lower:
            selected_articles.append(art.strip())

    # 4. Aggregate and Save to a New File
    if selected_articles:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Rejoin the filtered articles with '###' and line breaks for formatting
        output_content = "\n\n###\n\n" + "\n\n###\n\n".join(selected_articles)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        print(f"Filtering complete! Extracted {len(selected_articles)} articles.")
        print(f"Results saved to: {output_file_path}")
    else:
        print(f"No articles found containing the keyword '{target_keyword}'.")

if __name__ == "__main__":
    extract_articles()
