#!/usr/bin/env python3
"""
Term replacement script for creating unique knowledge base.
Replaces Lineage 2 terms with fictional equivalents.
"""

import json
import os
import re
from pathlib import Path


def load_terms_map(map_file="terms_map.json"):
    """Load term replacements from JSON file."""
    with open(map_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def replace_terms(text, terms_map):
    """
    Replace terms in text using the terms map.
    Uses word boundaries to avoid partial replacements.
    """
    # Sort terms by length (longest first) to avoid partial replacements
    sorted_terms = sorted(terms_map.items(), key=lambda x: len(x[0]), reverse=True)
    
    for original, replacement in sorted_terms:
        # Use word boundaries for exact word matching
        # Handle both singular and within compound words
        pattern = r'\b' + re.escape(original) + r'\b'
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def process_files(input_dir, output_dir, terms_map):
    """Process all text files in input directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process each .txt file
    files_processed = 0
    for txt_file in input_path.glob('*.txt'):
        print(f"Processing: {txt_file.name}")
        
        # Read original content
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace terms
        new_content = replace_terms(content, terms_map)
        
        # Write to output directory
        output_file = output_path / txt_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        files_processed += 1
        print(f"  → Saved to: {output_file}")
    
    return files_processed


def main():
    """Main execution function."""
    print("=" * 60)
    print("Knowledge Base Term Replacement Script")
    print("=" * 60)
    print()
    
    # Load terms mapping
    print("Loading terms map...")
    terms_map = load_terms_map()
    print(f"Loaded {len(terms_map)} term replacements")
    print()
    
    # Process files
    input_dir = "data/raw"
    output_dir = "knowledge_base"
    
    print(f"Processing files from: {input_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    files_count = process_files(input_dir, output_dir, terms_map)
    
    print()
    print("=" * 60)
    print(f"✓ Successfully processed {files_count} files")
    print(f"✓ Replaced {len(terms_map)} unique terms")
    print(f"✓ Output saved to: {output_dir}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
