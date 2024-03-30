import os
from bs4 import BeautifulSoup
from config import local_path

def read_interested_keys(file_path):
    """Reads interested keys from the given file."""
    with open(file_path, 'r') as file:
        keys = [line.strip() for line in file]
    return keys

def add_new_descriptions(content_dict, html_content, interested_keys):
    soup = BeautifulSoup(html_content, 'html.parser')
    current_h2_title = None
    elements = soup.find_all(['h2', 'h3', 'ul'])

    for element in elements:
        if element.name == "h2":
            current_h2_title = element.text.strip()
            content_dict.setdefault(current_h2_title, {})
        elif element.name == "h3":
            standard_key = element.text.strip()
            if current_h2_title:
                content_dict[current_h2_title].setdefault(standard_key, [])
        elif element.name == "ul" and current_h2_title:
            lis = element.find_all('li')
            for li in lis:
                description_text = li.text.strip()
                # Check if the description text contains any of the interested keys
                for key in interested_keys:
                    if key in description_text:
                        # Append the description text to the specific key in the current category
                        content_dict[current_h2_title].setdefault(key, []).append(description_text)

def print_content_structure(content_dict):
    for h2_title, standards in content_dict.items():
        print(f"\nCategory: {h2_title}")

        for key, descriptions in standards.items():
            print(f"  Standard {key}:")
            for description in descriptions:
                print(f"    - {description}")

def main():
    # Read interested keys from the file
    interested_keys = read_interested_keys('data_keys.txt')

    # Initialize the main dictionary to hold the structured content
    content_structure = {}

    # Specify the file to read HTML content from
    file_path = 'data_1_content_0.html'

    # Check if the file exists
    if os.path.exists(file_path):
        # Read HTML content from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

            # Add descriptions from the HTML content
            add_new_descriptions(content_structure, html_content, interested_keys)

            # Print the structured data
            #print_content_structure(content_structure)

            # Write the structured data to data_extracted.txt
            with open('data_extracted.txt', 'w') as outfile:
                for h2_title, standards in content_structure.items():
                    outfile.write(f"Category: {h2_title}\n")
                    for key, descriptions in standards.items():
                        outfile.write(f"  Standard {key}:\n")
                        for description in descriptions:
                            outfile.write(f"    - {description}\n")
                    outfile.write("-" * 40 + "\n")
    else:
        print(f"File '{file_path}' not found.")
