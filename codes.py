import re
import os

def run_conversion_single(file_path):
    # Read the content of the uploaded text file
    with open(file_path, 'r') as f:
        header_text = f.read()
    
    # Get the base filename
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Define regex patterns
    patterns = {
        "CLIENT": r"CLIENT:\s*(.*?)\s+COMPANY",
        "COMPANY": r"COMPANY:\s*(.*?)\s+PROJECT",
        "DATA TYPE": r"DATA TYPE:\s*(.*?)\s*;",
        "AREA": r"AREA:\s*(.*?)\s+PROJECT NO",
        "ACQUISITIN DATE": r"ACQUISITIN DATE:\s*(.*?)\s*;",
        "PROCESSING YEAR": r"PROCESSING YEAR\s*(.*?)$",
        "RECORD LENGTH": r"RECORD LENGTH:\s*(\d+MS)"
    }
    
    results = {"FILE NAME": file_name}
    
    for key, pattern in patterns.items():
        # Using re.MULTILINE and re.DOTALL to find text across lines
        match = re.search(pattern, header_text, re.MULTILINE)
        if match:
            results[key] = match.group(1).strip()
        else:
            results[key] = "NOT FOUND"
            
    return results