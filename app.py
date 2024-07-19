import re
import os
import zipfile
import shutil
from datetime import datetime

def parse_and_format_date(date_string):
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_string, "%a, %d %b, %Y")
        # Format the date as requested
        return date_obj.strftime("%B %d, %Y")
    except ValueError:
        # If parsing fails, return the original string
        return date_string

def process_file(input_file, export_folder):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into sections based on H1 headers
    sections = re.split(r'\n# ', content)

    for section in sections:
        if section.strip():
            # Extract the header (first line) as the filename and title
            lines = section.split('\n')
            title = lines[0].strip()
            filename = title + '.md'
            
            # Remove any characters that are not allowed in filenames
            filename = re.sub(r'[<>:"/\\|?*]', '', filename)
            
            # Process the content
            content = '\n'.join(lines[1:])
            
            # Remove '>' from lines starting with '>'
            content = re.sub(r'^> ', '', content, flags=re.MULTILINE)
            
            # Determine if it's a daily note and format the date
            date_match = re.match(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun), (\d{1,2} [A-Za-z]{3}, \d{4})', title)
            if date_match:
                formatted_date = parse_and_format_date(title)
                tag = "daily-jots"
            else:
                formatted_date = title
                tag = "imported"
            
            # Create frontmatter
            frontmatter = f"""---
title: {formatted_date}
tags:
  - {tag}
---

"""
            
            # Combine frontmatter and content
            full_content = frontmatter + content.strip()
            
            # Write the processed content to a new file in the export folder
            file_path = os.path.join(export_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(full_content)
            
            print(f"Created file: {file_path}")

def create_zip(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"Created zip file: {zip_name}")

if __name__ == "__main__":
    input_file = "Twos.md"
    export_folder = "export"
    zip_name = "export.zip"

    if os.path.exists(input_file):
        # Create export folder if it doesn't exist
        os.makedirs(export_folder, exist_ok=True)

        # Process the file and create individual markdown files
        process_file(input_file, export_folder)

        # Create a zip file of the export folder
        create_zip(export_folder, zip_name)

        # Optionally, remove the export folder after zipping
        # shutil.rmtree(export_folder)
    else:
        print(f"Error: The file {input_file} does not exist.")