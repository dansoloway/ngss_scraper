from bs4 import BeautifulSoup
import csv

def preprocess_html(html_content):
    # Remove all HTML tags
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator='\n', strip=True)
    return text_content

def split_by_keys(text_content, keys_file):
    with open(keys_file, 'r') as keys_file:
        keys = [key.strip() for key in keys_file.readlines()]

    split_content = {}
    current_key = None
    current_value = ''

    for line in text_content.split('\n'):
        line = line.strip()
        found_key = False
        for key in keys:
            if line.startswith(key):
                if current_key is not None:
                    split_content[current_key.rstrip('.')] = current_value.strip()
                    current_value = ''
                current_key = line
                found_key = True
                break
        if not found_key:
            current_value += line + ' '

    if current_key is not None:
        split_content[current_key.rstrip('.')] = current_value.strip()

    return split_content

def parse_html_to_csv(html_file, output_file, keys_file):
    # Open HTML file for reading
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

        print("HTML content before preprocessing:")
        print(html_content)
        
        # Preprocess HTML content
        preprocessed_html = preprocess_html(html_content)

        print("\nPreprocessed HTML content:")
        print(preprocessed_html)

        # Split preprocessed HTML content by keys
        split_content = split_by_keys(preprocessed_html, keys_file)

        print("\nSplit content:")
        print(split_content)

        # Open CSV file for writing
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['standard', 'question'])  # Write header

            for key, value in split_content.items():
                writer.writerow([key, value])

def main():
    # Specify the HTML file to read content from
    html_file = 'data_0_standards_0.html'

    # Specify the output file
    output_file = 'data_questions.csv'

    # Specify the file containing keys to split by
    keys_file = 'data_keys.txt'

    # Parse HTML content and write to CSV
    parse_html_to_csv(html_file, output_file, keys_file)

    print(f"\nCSV file '{output_file}' has been created successfully.")

if __name__ == "__main__":
    main()
