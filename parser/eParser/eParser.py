import os
from constants import client_folder, server_folder
from parsing import *
from file_management import *
from tablemaker import *


# List of tuples containing the following data for each test scenario:
#   - description:    dict
#   - client_results: dict
#   - server_results: dict or None
#   - query_messages: list (of dicts) or None
test_data = list()


# Parse all test scenarios and store the data in the list
for test_folder in os.listdir(client_folder):
    test_folder_client = os.path.join(client_folder, test_folder)

    # Check if test folder is valid (contains test_description.xml and test_results.xml)
    if False == validate_test_folder(test_folder_client):
        continue
    print(f'Processing test scenario {test_folder}...')

    # Check if server data exists
    server_data = check_server_data(server_folder, test_folder)
    if server_data:
        test_folder_server = os.path.join(server_folder, test_folder)

    # Parse the test description file
    description = parse_description_file(test_folder_client)

    # Parse the test results files
    client_results = parse_result_file(test_folder_client)
    if server_data:
        server_results = parse_result_file(test_folder_server)
    else:
        server_results = None

    # Parse the query messages
    query_messages = parse_query_messages(test_folder_client)

    test_data.append((description, client_results, server_results, query_messages))


# Sort the list after 'cycle_time' and then after 'datagram_size' (both in description)
test_data.sort(key=lambda x: (x[0]['connection']['datagram_size'], x[0]['connection']['cycle_time']))
    

# Write the test data to a csv file
write_test_table(test_data)
