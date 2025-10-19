"""
### File: test/encodings.py

Checks if the project is encoded in ASCII.
Only for testing purposes.
"""

# just search [^\x00-\x7F] with regex match

__author__ = 'Sufiyan Attar'
__version__ = '1.0.0'
__maintainer__ = 'Sufiyan Attar'
__email__ = 'sufiyan.attar@gmail.com'
__status__ = 'Development'

EXCLUDED_EXTENTIONS = [
    '.ico', 
    '.png',
    # '.md', 
    '.ini'
]
EXCLUDED_FOLDERS = [
    '__pycache__', 
    'venv', 
    '.git', 
    'node_modules', 
    '.next'
]

import os

target_folder = r'D:\project\instagram'
target_folder = r'C:\Users\Sufiyan Attar\Documents\instagram\backend'
show_each_line = False  # <<< set to False if you want only file name and line number

def find_non_ascii_lines(content):
    lines_with_non_ascii = []
    for i, line in enumerate(content.splitlines(), start=1):
        non_ascii = [c for c in line if ord(c) >= 128]
        if non_ascii:
            lines_with_non_ascii.append((i, non_ascii))
    return lines_with_non_ascii

def is_ascii_file(file_path):
    encodings_to_try = ['utf-8', 'utf-16', 'latin1']  # latin1 handles anything without error

    for enc in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
                non_ascii_lines = find_non_ascii_lines(content)
                if non_ascii_lines:
                    return False, non_ascii_lines
                return True, []
        except Exception:
            continue
    return False, [('?', ['non readable characters'])]

def check_ascii_in_folder(root_folder):
    found_non_ascii = False
    for dirpath, _, filenames in os.walk(root_folder):
        if any(exclude in dirpath for exclude in EXCLUDED_FOLDERS):
            continue
        for file in filenames:
            if any(excluded in file for excluded in ['File Structure']):
                continue
            full_path = os.path.join(dirpath, file)
            if any(file.endswith(excluded_extention) for excluded_extention in EXCLUDED_EXTENTIONS):
                continue
            if any(file.startswith(excluded_prefix) for excluded_prefix in ['mnbvbwrj']):
                continue

            is_ascii, non_ascii_info = is_ascii_file(full_path)
            if not is_ascii:
                found_non_ascii = True
                if show_each_line:
                    for line_no, chars in non_ascii_info:
                        print(f'NON-ASCII at {full_path}:{line_no} -> {chars}')
                else:
                    print(f'NON-ASCII in "{full_path}": {non_ascii_info}')
    if not found_non_ascii:
        print('All files are ASCII')

check_ascii_in_folder(target_folder)
