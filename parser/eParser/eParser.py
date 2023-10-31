import os
from datetime import datetime
from constants import client_folder, server_folder, output_folder, concurrent_execution
from parsing import parse_description_file, parse_result_file, parse_query_messages
from file_management import validate_test_folder, check_server_data
from tablemaker import write_test_table, write_query_table
from graphs import create_campaign_graphs, create_scenario_graphs, create_datagramsize_graphs


campaign_name = 'test'

# Check if the results folder exists
if not os.path.exists(client_folder):
    print(f'ERROR: Folder {client_folder} does not exist!')
    exit(1)

# Print start message
print(f'Starting eParser... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

# Create campaign folder for the output
current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
campaign_folder = os.path.join(output_folder, f"{campaign_name}_{current_timestamp}")
if not os.path.exists(campaign_folder):
    os.makedirs(campaign_folder)


# List of tuples containing the following data for each test scenario:
#   - description:    dict
#   - client_results: dict
#   - server_results: dict or None
#   - query_messages: list (of dicts) or None
test_data = list()
processes = list()

# Parse all test scenarios and store the data in the list
for test_folder in os.listdir(client_folder):
    test_folder_client = os.path.join(client_folder, test_folder)

    # Check if test folder is valid (contains test_description.xml and test_results.xml)
    if not validate_test_folder(test_folder_client):
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


# Write the test data to a csv file and create query overview if possible
write_test_table(test_data, campaign_name, campaign_folder, processes)
write_query_table(test_data, campaign_folder, processes)


# Create graphs:
#   - campaign
#   - scenario (only if query messages are available)
create_campaign_graphs(test_data, campaign_folder, processes)
create_scenario_graphs(test_data, campaign_folder, processes)
create_datagramsize_graphs(test_data, campaign_folder, processes)


# End the execution of eParser
if concurrent_execution:
    for process in processes:
        process.join()

print(f'Finished eParser... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
