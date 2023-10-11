import os
import xml.etree.ElementTree as ET
import pandas as pd

# Define the root folder where test folders are located
root_folder = 'results'

# Create an empty list to store data dictionaries for each test
all_test_data = []

# Initialize a set to store all unique XML tags
all_tags = set()

# Iterate through the subfolders in the root folder
for test_folder in os.listdir(root_folder):
    test_folder_path = os.path.join(root_folder, test_folder)

    # Check if the item in the root folder is a directory
    if os.path.isdir(test_folder_path):
        # Find and parse the test_description.xml file
        description_file_path = os.path.join(test_folder_path, 'test_description.xml')
        results_file_path = os.path.join(test_folder_path, 'test_results.xml')

        if os.path.exists(description_file_path) and os.path.exists(results_file_path):
            tree_description = ET.parse(description_file_path)
            root_description = tree_description.getroot()

            tree_results = ET.parse(results_file_path)
            root_results = tree_results.getroot()

            # Extract and combine the XML data from both files
            data = {}

            # Function to create unique column names based on parent tags
            def get_unique_column_name(parent_tag, child_tag):
                return f"{parent_tag}_{child_tag}"

            # Process elements in test_description.xml
            for element in root_description.iter():
                if element.text is not None:
                    tag_name = element.tag
                    all_tags.add(tag_name)
                    data[tag_name] = element.text
                    for child in element:
                        child_tag = get_unique_column_name(tag_name, child.tag)
                        all_tags.add(child_tag)
                        data[child_tag] = child.text

            # Process elements in test_results.xml
            for element in root_results.iter():
                if element.text is not None:
                    tag_name = element.tag
                    all_tags.add(tag_name)
                    data[tag_name] = element.text
                    for child in element:
                        child_tag = get_unique_column_name(tag_name, child.tag)
                        all_tags.add(child_tag)
                        data[child_tag] = child.text

            all_test_data.append(data)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(all_test_data)

# Write the DataFrame to an Excel file
output_excel_file = 'combined_test_data.xlsx'
df.to_excel(output_excel_file, index=False)

print(f"Data from {len(all_test_data)} tests have been stored in {output_excel_file}.")

# Save the unique XML tags to a separate CSV file
tags_csv_file = 'unique_xml_tags.csv'
with open(tags_csv_file, 'w') as file:
    for tag in all_tags:
        file.write(f"{tag}\n")

print(f"Unique XML tags have been stored in {tags_csv_file}.")
