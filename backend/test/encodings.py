"""
File: test/encodings.py

Checks if the project is encoded in ASCII.
Only for testing purposes.
"""

import os

def find_non_ascii(content):
    non_ascii_chars = [char for char in content if ord(char) >= 128]
    return non_ascii_chars

def is_ascii_file(file_path):
    encodings_to_try = ['utf-8', 'utf-16', 'latin1']  # latin1 handles anything without error
    
    for enc in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
                non_ascii_chars = find_non_ascii(content)
                if non_ascii_chars:
                    return False, non_ascii_chars
                return True, []
        except Exception:
            continue
    return False, ['non readable characters']

def check_ascii_in_folder(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        if any(exclude in dirpath for exclude in ['__pycache__', 'venv', '.git']):
            continue
        for file in filenames:
            if any(excluded in file for excluded in ['File Structure', 'yet.ini', 'README.md']):
                continue
            full_path = os.path.join(dirpath, file)
            if any(file.endswith(excluded_extention) for excluded_extention in ['.ico', '.png']):
                continue
            is_ascii, non_ascii_chars = is_ascii_file(full_path)
            if not is_ascii:
                print(f'NON-ASCII in "{full_path}": {non_ascii_chars}')

check_ascii_in_folder(r'D:\project\instagram')
