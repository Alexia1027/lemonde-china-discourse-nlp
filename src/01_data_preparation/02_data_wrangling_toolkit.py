"""
Data Wrangling Toolkit for Le Monde Corpus
------------------------------------------
This module provides utility functions for preprocessing raw text data, 
including splitting docx files, merging text files, and extracting 
specific subsets of articles based on target titles.
"""

import os
import re
from docx import Document

def split_docx_to_txt(input_docx_path, output_dir):
    """
    Reads a .docx file and splits it into multiple .txt files based on the '###' delimiter.
    The first line of each section is used as the filename.
    """
    print(f"Starting to split docx: {input_docx_path}")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        doc = Document(input_docx_path)
    except Exception as e:
        print(f"Error loading document: {e}")
        return

    # Extract non-empty paragraphs
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip() != ""]
    current_section = []
    successful_files = 0
    
    for paragraph in paragraphs:
        if "###" in paragraph:
            if current_section:
                # Use the first line as the filename, default to section_number if empty
                first_line = current_section[0].strip()
                if not first_line:
                    first_line = f"section_{successful_files + 1}"

                # Clean filename to prevent OS errors
                safe_name = re.sub(r'[\\/*?:"<>|]', '_', first_line)
                file_name = f"{safe_name}.txt"
                file_path = os.path.join(output_dir, file_name)

                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write("\n".join(current_section).strip())
                    successful_files += 1
                except Exception as e:
                    print(f"Failed to save {file_name}. Error: {e}")

            # Reset for the next section
            current_section = []
        else:
            current_section.append(paragraph)
            
    # Save the last section if any remains
    if current_section:
        first_line = current_section[0].strip()
        if not first_line:
            first_line = f"section_{successful_files + 1}"

        safe_name = re.sub(r'[\\/*?:"<>|]', '_', first_line)
        file_path = os.path.join(output_dir, f"{safe_name}.txt")

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("\n".join(current_section).strip())
            successful_files += 1
        except Exception as e:
            print(f"Failed to save final section. Error: {e}")

    if successful_files > 0:
        print(f"Successfully split into {successful_files} TXT files!")


def merge_txt_files(input_dir, output_file_path):
    """
    Merges all .txt files in a given directory into a single text file,
    separated by double line breaks.
    """
    print(f"Merging files from: {input_dir}")
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        count = 0
        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write('\n\n###\n\n') # Keep delimiter for downstream tasks
                count += 1
                
    print(f"Successfully merged {count} TXT files into: {output_file_path}")


def extract_articles_by_titles(source_file_path, output_file_path, target_titles_str):
    """
    Extracts specific articles from a large corpus file by matching 
    the first line (title) against a provided list of target titles.
    """
    # 1. Preprocess the target titles
    target_titles = [line.strip().lower() for line in target_titles_str.split('\n') if line.strip()]
    target_set = set(target_titles)
    print(f"Target articles to extract: {len(target_set)}")

    # 2. Read the full corpus
    if not os.path.exists(source_file_path):
        print(f"Error: Source file not found -> {source_file_path}")
        return

    with open(source_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Split by delimiter
    raw_articles = [art.strip() for art in content.split('###') if art.strip()]
    matched_articles = []
    found_titles = set()

    # 4. Iterate and match
    for art in raw_articles:
        lines = art.split('\n')
        if not lines:
            continue
            
        first_line = lines[0].strip().lower()
        
        # Check if the title is in our target set
        if first_line in target_set:
            matched_articles.append(art)
            found_titles.add(first_line)

    # 5. Export results
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("###\n\n" + "\n\n###\n\n".join(matched_articles))

    # 6. Print extraction report
    print("\n--- Extraction Report ---")
    print(f"Total articles in corpus: {len(raw_articles)}")
    print(f"Successfully matched and exported: {len(matched_articles)} articles")
    
    missing = target_set - found_titles
    if missing:
        print(f"Missing titles ({len(missing)}):")
        for m in sorted(list(missing)):
            print(f"  - {m}")
    else:
        print("Success! All specified titles were found and extracted.")

# ==========================================
# Example Usage (Commented out for safety)
# ==========================================
if __name__ == "__main__":
    pass
    # --- Example 1: Split ---
    # split_docx_to_txt("../data/raw/2023.2.docx", "../data/interim/split_files/")
    
    # --- Example 2: Merge ---
    # merge_txt_files("../data/interim/split_files/", "../data/processed/merged_corpus.txt")
    
    # --- Example 3: Extract ---
    # sample_titles = "Title 1\nTitle 2\nTitle 3"
    # extract_articles_by_titles("../data/processed/merged_corpus.txt", "../data/processed/subset.txt", sample_titles)
