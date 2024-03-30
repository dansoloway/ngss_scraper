import os
from bs4 import BeautifulSoup
from config import local_path

def parse_standard_key(key):
    """Extracts numeric part from a standard key for sorting."""
    parts = key.split('-')
    try:
        return int(parts[-1])
    except ValueError:
        # Return original key if it doesn't end with a number
        return float('inf')  # Place non-numeric keys at the end

def add_new_descriptions(content_dict, html_content):
    """Parses HTML content and adds new descriptions under the appropriate standards."""
    soup = BeautifulSoup(html_content, 'html.parser')
    table_rows = soup.find_all('tr')

    for row in table_rows:
        standard_key = row.find('th').text.strip('.')
        if standard_key not in content_dict:
            content_dict[standard_key] = []

        # Find all `<span class="popup">` within this row for detailed descriptions
        popups = row.find_all('span', class_='popup')
        for popup in popups:
            if 'title' in popup.attrs:
                title_content_html = popup['title']
                title_content_soup = BeautifulSoup(title_content_html, 'html.parser')
                description_text = title_content_soup.get_text(separator=' ', strip=True)
                content_dict[standard_key].append(description_text)

def print_standard_keys(content_dict):
    """Prints just the standard keys, sorted."""
    sorted_keys = sorted(content_dict.keys(), key=parse_standard_key)
    for key in sorted_keys:
        print(key)

def main():
    # Initialize the main dictionary to hold the structured content
    content_structure = {}

    # Specify the file to process
    file_name = "data_0_standards_0.html"
    file_path = os.path.join(local_path, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        # Read HTML content from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            # Parse the HTML content and populate the content structure dictionary
            add_new_descriptions(content_structure, html_content)

        # Specify the output file path
        output_file_path = os.path.join(local_path, "data_keys.txt")

        # Write standard keys to the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            sorted_keys = sorted(content_structure.keys(), key=parse_standard_key)
            for key in sorted_keys:
                output_file.write(key + '\n')
                # Print the key to the console
                print(key)

        print(f"Standard keys written to '{output_file_path}' and printed to console.")
    else:
        print(f"File '{file_name}' not found.")
