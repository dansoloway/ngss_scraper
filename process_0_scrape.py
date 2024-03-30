import os
import requests
from bs4 import BeautifulSoup
from config import local_path

def save_content_to_file(file_name, content):
    # Prepend the local_path to the file name
    full_path = os.path.join(local_path, file_name)
    # Open the file in write mode ('w') to overwrite existing content
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(str(content))
    print(f"File '{file_name}' saved successfully.")

def main(target_url):
    response = requests.get(target_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # New block to handle 'page-header'
        page_header = soup.find(class_="page-header")
        if page_header:
            header_text = page_header.get_text(strip=True)
            save_content_to_file('date_header.txt', header_text)

        rows2 = soup.find_all(class_="row2")
        rows3 = soup.find_all(class_="row3")

        files_processed = 0  # Counter for files processed
        
        for i, row in enumerate(rows2):
            file_name = f'data_0_standards_{i}.html'
            save_content_to_file(file_name, row)
            files_processed += 1  # Increment counter
        
        for i, row in enumerate(rows3):
            file_name = f'data_1_content_{i}.html'
            save_content_to_file(file_name, row)
            files_processed += 1  # Increment counter

        if files_processed > 0:
            print("Content saved successfully.")
        else:
            print("No new content found.")
    else:
        print("Failed to retrieve the webpage")

if __name__ == "__main__":
    # If the script is executed directly, run the main function with the target_url
    main("https://www.nextgenscience.org/dci-arrangement/hs-ls3-heredity-inheritance-and-variation-traits")
