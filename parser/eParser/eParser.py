import os
from multiprocessing import Process
from datetime import datetime
from constants import client_folder, server_folder, output_folder
from parsing import *
from file_management import *
from tablemaker import write_test_table, write_query_table
from graphs import *


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
    

# Write the test data to a csv file and create query overview if possible
write_test_table(test_data, campaign_folder, processes)
write_query_table(test_data, campaign_folder, processes)


# Create graphs:
#   - campaign
#       - packet loss per datagram size
#       - packet loss per test case (colored bars)
#   - test scenario
#       - packet drops (per X) histogram
#       - packet drops over time

plot_campaign_loss_per_datagram_size(test_data, campaign_folder)
plot_campaign_loss_per_cycle_time(test_data, campaign_folder)       # FIXME: not implemented

for test_scenario in test_data:
    if test_scenario[3] is not None:
        scenario_path = os.path.join(campaign_folder, f"{test_scenario[0]['metadata']['t_uid']}")

        process = Process(target=create_scenario_graphs, args=(test_scenario, scenario_path))
        process.start()
        processes.append(process)

for process in processes:
    process.join()

 
# Print end message
print(f'Finished eParser... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')