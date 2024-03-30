import os
import csv

def read_date_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def read_csv_to_dict(file_path):
    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        return list(reader)

def create_synthesis(title, questions, dimensions):
    synthesis = title + '\n\n'
    
    # Ensure dimensions are sorted by standard for consistent output
    dimensions.sort(key=lambda x: x['standard'])
    
    for question in questions:
        standard = question['standard']
        synthesis += f"{standard}: {question['question']}\n\n"
        
        related_dimensions = [dim for dim in dimensions if dim['standard'] == standard]
        for dim in related_dimensions:
            synthesis += f"- {dim['category']}: {dim['description']}\n"
        
        synthesis += '\n'  # Extra newline for spacing between standards
    
    return synthesis

def main():
    # File paths
    date_header_path = 'date_header.txt'
    questions_path = 'data_questions.csv'
    dimensions_path = 'data_dimensions.csv'
    
    # Read data from files
    title = read_date_header(date_header_path)
    questions = read_csv_to_dict(questions_path)
    dimensions = read_csv_to_dict(dimensions_path)
    
    # Create synthesis
    synthesis = create_synthesis(title, questions, dimensions)
    
    # Output to a text file or print
    #print(synthesis)
    #Optionally, write to a file
    with open('synthesis_output.txt', 'w', encoding='utf-8') as out_file:
        out_file.write(synthesis)
    print("Synthesis created successfully.")
if __name__ == "__main__":
    main()
