import os
from multiprocessing import Process
from constants import concurrent_execution
from graphs_campaign import _prepare_and_create_campaign_graphs
from graphs_scenario import _prepare_and_create_scenario_graphs


def create_campaign_graphs(test_data: list, campaign_folder: str, processes: list = None) -> None:
    '''
    Creates the graphs for the campaign. This includes:
        - Packet loss per datagram size
        - Packet loss per cycle time

            Parameters:
                    test_data (list): List of parsed test scenarios
                    campaign_folder (str): Path to the folder where the table should be saved
                    processes (list): List of processes (optional, used for concurrent execution)

            Returns:
                    None
    '''
    if concurrent_execution:
        process = Process(target=_prepare_and_create_campaign_graphs, args=(test_data, campaign_folder))
        process.start()
        processes.append(process)
    else:
        _prepare_and_create_campaign_graphs(test_data, campaign_folder)



#                                _                               _
#                               (_)                             | |
#  ___  ___ ___ _ __   __ _ _ __ _  ___     __ _ _ __ __ _ _ __ | |__  ___
# / __|/ __/ _ \ '_ \ / _` | '__| |/ _ \   / _` | '__/ _` | '_ \| '_ \/ __|
# \__ \ (_|  __/ | | | (_| | |  | | (_) | | (_| | | | (_| | |_) | | | \__ \
# |___/\___\___|_| |_|\__,_|_|  |_|\___/   \__, |_|  \__,_| .__/|_| |_|___/
#                                           __/ |         | |
#                                          |___/          |_|

def create_scenario_graphs(test_data: list, campaign_folder: str, processes: list = None) -> None:
    '''
    Creates the graphs for each test scenario. This includes:
        - Histogram of packet losses
        - Packet losses over time
        - Sent and received packets over time
        - Packets per second over time / Packets per query over time

    Note that the diagrams are only created if the test scenario contains query messages. Otherwise
    the diagrams are skipped.

            Parameters:
                    test_data (list): List of parsed test scenarios
                    campaign_folder (str): Path to the folder where the table should be saved
                    processes (list): List of processes (optional, used for concurrent execution)

            Returns:
                    None
    '''
    for test_scenario in test_data:
        if test_scenario[3] is not None:
            scenario_path = os.path.join(campaign_folder, f"{test_scenario[0]['metadata']['t_uid']}")

            if concurrent_execution:
                process = Process(target=_prepare_and_create_scenario_graphs, args=(test_scenario, scenario_path))
                process.start()
                processes.append(process)
            else:
                _prepare_and_create_scenario_graphs(test_scenario, scenario_path)
