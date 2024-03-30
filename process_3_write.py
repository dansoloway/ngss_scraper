import csv

def parse_input_to_csv_rows(input_text, keys):
    rows = []
    current_category = ""
    current_standard = ""
    for line in input_text.strip().split('\n'):
        line = line.strip()
        if line.startswith("-") and not line.startswith("- "):
            continue
        if line.startswith("Category:"):
            current_category = line.split("Category:", 1)[1].strip()
        elif line.startswith("Standard"):
            current_standard = line.split("Standard", 1)[1].strip().rstrip(":")
        elif line.startswith("-"):
            description = line[1:].strip()
            rows.append([current_standard, current_category, description])
        else:
            continue
    return rows

def parse_input_to_csv_rows_with_single_key(input_text, key):
    rows = []
    current_category = ""
    for line in input_text.strip().split('\n'):
        line = line.strip()
        if line.startswith("Category:"):
            current_category = line.split("Category:", 1)[1].strip()
        elif line.startswith("Standard"):
            standard_name = line.split("Standard", 1)[1].strip().rstrip(":")
            if standard_name:
                rows.append([key, current_category, standard_name])
    return rows

def write_to_csv(filename, rows):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["standard", "category", "description"])
        for row in rows:
            writer.writerow(row)
    return len(rows)

def main():
    with open("data_extracted.txt", "r") as file:
        input_text = file.read()

    with open("data_keys.txt", "r") as key_file:
        keys = [key.strip() for key in key_file.readlines()]

    if len(keys) == 1:
        parsed_rows = parse_input_to_csv_rows_with_single_key(input_text, keys[0])
    else:
        parsed_rows = parse_input_to_csv_rows(input_text, keys)

    #print("Parsed Rows:")
    #for row in parsed_rows:
        #print(row)

    num_rows_written = write_to_csv("data_dimensions.csv", parsed_rows)
    print(f"CSV file has been created with {num_rows_written} rows.")

if __name__ == "__main__":
    main()
