import xml.etree.ElementTree as ET
import pandas as pd
import os
import matplotlib.pyplot as plt

def get_t_uid(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the "t_uid" element and extract its text as the file name
    t_uid_element = root.find(".//metadata/t_uid")
    if t_uid_element is not None:
        return t_uid_element.text
    else:
        return None
    
def create_histogram_loss_vs_occurence(data_dict, histogram_image_file):
    misses = list(data_dict.keys())
    occurrences = list(data_dict.values())

    # Create a histogram
    plt.figure(figsize=(8, 6))
    plt.bar(misses, occurrences, color='skyblue', width=0.6, align='center', edgecolor='black')
    plt.xlabel('Misses', fontsize=12)
    plt.ylabel('Occurrences', fontsize=12)
    plt.title('Misses vs. Occurrences Histogram per 100000 Datagr (CHANGE TITLE!)', fontsize=16)
    
    # Add horizontal grid lines
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the histogram as an image file
    plt.savefig(histogram_image_file)

def create_histogram_time_vs_loss(data_dict, histogram_image_file):
    time = list(data_dict.keys())
    losses = list(data_dict.values())

    # Create a histogram
    plt.figure(figsize=(8, 6))
    plt.bar(time, losses, color='skyblue', width=0.6, align='center', edgecolor='black')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Losses', fontsize=12)
    plt.title('Time vs. Losses Diagram', fontsize=16)

    # Add horizontal grid lines
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the histogram as an image file
    plt.savefig(histogram_image_file)



# Define a function to parse XML data and extract "misses" and "total" entries
def parse_xml_to_dataframe(xml_file, diagr_occ, diagr_time):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = []
    occurence_vs_loss = {}
    time_vs_loss = {0: 0}

    for report in root.findall(".//query/report"):

        # Parse the Report entries
        total = int(report.find("misses").text)
        misses = int(report.find("total").text)
        timestamp_element = report.find('timestamp')
        if timestamp_element is not None:
            timestamp = float(timestamp_element.text)
        else:
            timestamp = 0.0

        # Calculate the difference between the current and previous "misses" entries
        diff = misses - (data[-1][2] if len(data) > 0 else 0)
        if(diff < 0):
            diff = 0
            misses = data[-1][2]

        # Add the difference to the dictionary    
        occ = occurence_vs_loss.get(diff, 0)
        occurence_vs_loss[diff] = (occ + 1)
        
        # Add the timestamp to the dictionary
        time_vs_loss[timestamp] = diff

        # Append the extracted data to the list
        data.append([timestamp, total, misses, diff])

    # Create a DataFrame with the extracted data
    create_histogram_loss_vs_occurence(occurence_vs_loss, diagr_occ)
    create_histogram_time_vs_loss(time_vs_loss, diagr_time)
    df = pd.DataFrame(data, columns=["timestamp", "total_datagram", "total_misses", "difference"])
    return df





# Define the root folder where test folders are located
root_folder = 'results'
result_folder = 'output'

# Iterate through the subfolders in the root folder
for test_folder in os.listdir(root_folder):
    test_folder_path = os.path.join(root_folder, test_folder)

    # Check if the item in the root folder is a directory
    if os.path.isdir(test_folder_path):
        # Find and parse the test_description.xml file
        description_file_path = os.path.join(test_folder_path, 'test_description.xml')
        results_file_path = os.path.join(test_folder_path, 'test_results.xml')

        if os.path.exists(description_file_path) and os.path.exists(results_file_path):
            t_uid = get_t_uid(description_file_path)

            results_path = os.path.join(result_folder, t_uid)
            if not os.path.exists(results_path):
                os.makedirs(results_path)

            df = parse_xml_to_dataframe(results_file_path, os.path.join(results_path, 'diagr_occ.png'), os.path.join(results_path, 'diagr_time.png'))
            df.to_excel(os.path.join(results_path, 'query.xlsx'), index=False)

print('Done!')
            
            






