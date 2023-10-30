import os
import math
from multiprocessing import Process
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
import numpy as np
import seaborn as sns
from constants import generate_histogram, generate_latex, generate_png, concurrent_execution
from data_format import format_query


#                                  _                                     _
#                                 (_)                                   | |
#   ___ __ _ _ __ ___  _ __   __ _ _  __ _ _ __     __ _ _ __ __ _ _ __ | |__  ___
#  / __/ _` | '_ ` _ \| '_ \ / _` | |/ _` | '_ \   / _` | '__/ _` | '_ \| '_ \/ __|
# | (_| (_| | | | | | | |_) | (_| | | (_| | | | | | (_| | | | (_| | |_) | | | \__ \
#  \___\__,_|_| |_| |_| .__/ \__,_|_|\__, |_| |_|  \__, |_|  \__,_| .__/|_| |_|___/
#                     | |             __/ |         __/ |         | |
#                     |_|            |___/         |___/          |_|

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
        process = Process(target=__prepare_and_create_campaign_graphs, args=(test_data, campaign_folder))
        process.start()
        processes.append(process)
    else:
        __prepare_and_create_campaign_graphs(test_data, campaign_folder)


def __prepare_and_create_campaign_graphs(test_data: list, campaign_folder: str) -> None:
    __plot_campaign_loss_per_datagram_size(test_data, campaign_folder)
    __plot_campaign_diagr2(test_data, campaign_folder)


def __plot_campaign_loss_per_datagram_size(test_data: list, output_path: str) -> None:
    diagram_name = 'campaign-diagr1__cases_by_losses_and_datagram'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    x_labels = ['0', ']0;10]', ']10;20]', ']20;30]', ']30;40]', ']40;50]', ']50;60]', ']60;70]', ']70;80]', ']80;90]', ']90;100]']
    losses_per_size = dict()

    # Get all packet sizes
    for test_scenario in test_data:
        datagram_size = test_scenario[0]['connection']['datagram_size']
        loss_ratio = (test_scenario[1]['report']['losses'] / test_scenario[1]['report']['total']) * 100

        loss_list = losses_per_size.get(datagram_size, list([0]*len(x_labels)))
        if loss_ratio == 0:
            loss_list[0] += 1
        elif loss_ratio <= 10:
            loss_list[1] += 1
        elif loss_ratio <= 20:
            loss_list[2] += 1
        elif loss_ratio <= 30:
            loss_list[3] += 1
        elif loss_ratio <= 40:
            loss_list[4] += 1
        elif loss_ratio <= 50:
            loss_list[5] += 1
        elif loss_ratio <= 60:
            loss_list[6] += 1
        elif loss_ratio <= 70:
            loss_list[7] += 1
        elif loss_ratio <= 80:
            loss_list[8] += 1
        elif loss_ratio <= 90:
            loss_list[9] += 1
        else:
            loss_list[10] += 1

        losses_per_size[datagram_size] = loss_list

    sorted_losses_per_size = {k: losses_per_size[k] for k in sorted(losses_per_size, reverse=False)}


    # Create a bar chart for each datagram size
    bar_width = 0.2
    colors = ['lightgray', 'steelblue', '#9fcc9f', '#ffb3e6']   # colors for the bars
    index = np.arange(len(x_labels))

    _, ax = plt.subplots(figsize=(12, 5))
    for idx, (size, values) in enumerate(sorted_losses_per_size.items()):
        ax.bar(index + bar_width * idx, values, bar_width, color=colors[idx % len(colors)], edgecolor='black', label=f"{size} Byte", alpha=0.7)

    # Add axis labels and titles
    ax.set_title('Test Cases by Packet Loss Ratio and Datagram Size (across all Cycle Times)')
    ax.set_xlabel('Packet Loss Ratio')
    ax.set_ylabel('Test Cases')
    ax.legend(loc='upper right', frameon=True, title='Datagram Size')
    ax.set_xticks(index + bar_width, [f"{x_label} %" for x_label in x_labels])
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    max_value = max([max(values) for values in sorted_losses_per_size.values()])
    plt.ylim(0, math.ceil(max_value / 0.78))

    plt.tight_layout()

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if generate_png:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    plt.close()


def __plot_campaign_diagr2(test_data: list, output_path: str) -> None:
    diagram_name = 'campaign-diagr2__losses_by_cycle_and_datagram'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    cycle_times = sorted(list(set(test_scenario[0]['connection']['cycle_time'] for test_scenario in test_data)))
    losses_per_size = dict()

    # Get all packet sizes
    for test_scenario in test_data:
        current_datagram_size = test_scenario[0]['connection']['datagram_size']
        current_cycle_time = test_scenario[0]['connection']['cycle_time']
        current_loss_ratio = (test_scenario[1]['report']['losses'] / test_scenario[1]['report']['total']) * 100

        current_loss_list = losses_per_size.get(current_datagram_size, list([0]*len(cycle_times)))
        for idx, cycle_time in enumerate(cycle_times):
            if cycle_time == current_cycle_time:
                current_loss_list[idx] = current_loss_ratio

        losses_per_size[current_datagram_size] = current_loss_list

    sorted_losses_per_size = {k: losses_per_size[k] for k in sorted(losses_per_size, reverse=False)}

    # Create a bar chart for each datagram size
    bar_width = 0.2
    colors = ['lightgray', 'steelblue', '#9fcc9f', '#ffb3e6']   # colors for the bars
    index = np.arange(len(cycle_times))

    bars = list()
    _, ax = plt.subplots(figsize=(12, 5))
    for idx, (size, values) in enumerate(sorted_losses_per_size.items()):
        bars.append(ax.bar(index + bar_width * idx, values, bar_width, color=colors[idx % len(colors)], edgecolor='black', label=f"{size} Byte", alpha=0.7))

    for record in bars:
        for entry in record:
            yval = entry.get_height()
            plt.text(entry.get_x() + entry.get_width()/2., yval + 0.01, f"{yval:.2f}%", ha='center', va='bottom')

    # Add axis labels and titles
    ax.set_title('Packet Losses by Cycle Time and Datagram Size')
    ax.set_xlabel('Cycle Time')
    ax.set_ylabel('Packet Loss Ratio')
    ax.legend(loc='upper right', frameon=True, title='Datagram Size')
    ax.set_xticks(index + bar_width, [f"{(cycle_time / 1000):.1f} \u03bcs" for cycle_time in cycle_times])

    max_value = max([max(values) for values in sorted_losses_per_size.values()])
    plt.ylim(0, math.ceil(max_value / 0.78))

    def percent_formatter(x, _):
        return f"{x:.0f}%"
    plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

    plt.tight_layout()

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if generate_png:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    plt.close()


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
                process = Process(target=__prepare_and_create_scenario_graphs, args=(test_scenario, scenario_path))
                process.start()
                processes.append(process)
            else:
                __prepare_and_create_scenario_graphs(test_scenario, scenario_path)


def __prepare_and_create_scenario_graphs(test_scenario: tuple, output_path: str) -> None:
    query = format_query(test_scenario[3].copy(), test_scenario[1]['report']['duration'], test_scenario[1]['report']['losses'], test_scenario[1]['report']['total'])
    current_scenario = (test_scenario[0], test_scenario[1], test_scenario[2], query)

    __plot_scenario_histogram_losses(current_scenario, output_path)
    __plot_scenario_losses_over_time(current_scenario, output_path)
    __plot_scenario_packages_over_time(current_scenario, output_path)
    __plot_scenario_pps_over_time(current_scenario, output_path)
    __plot_scenario_ppq_over_time(current_scenario, output_path)


def __plot_scenario_histogram_losses(test_scenario: tuple, output_path: str) -> None:
    if not generate_histogram:
        return

    diagram_name = 'histogram_losses'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3]

    # Get the data for the histogram
    differences_list = [report['difference'] for report in query]

    # Create the histogram
    # Creating the histogram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.hist(differences_list, bins=range(0, max(differences_list) + 2), align='left', color='steelblue', edgecolor='black', alpha=0.7)

    # Labels, title, and other configurations
    ax.set_xlabel('Packet Losses per 100000 Packets (Number of Packets)')
    ax.set_ylabel('Frequency')
    # ax.set_yscale('log')
    ax.set_title('Frequency Analysis of Packet Losses')
    ax.set_xticks(range(0, max(differences_list) + 10, 10))
    plt.tight_layout()

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if generate_png:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    plt.close()


def __plot_scenario_losses_over_time(test_scenario: tuple, output_path: str) -> None:
    diagram_name = 'losses_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3].copy()
    query.insert(0, {'timestamp': 0, 'total': 0, 'losses': 0, 'difference': 0})

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    difference = [report['difference'] for report in query]

    # Create the diagram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, difference, color='lightgray', edgecolor='black', alpha=0.6)
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Lost Packets (Number of Packets)')
    # ax.set_yscale('log')
    ax.set_title('Temporal Distribution of Packet Loss')

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if generate_png:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    plt.close()


def __plot_scenario_packages_over_time(test_scenario: tuple, output_path: str) -> None:
    diagram_name = 'packages_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3].copy()
    query.insert(0, {'timestamp': 0, 'total': 0, 'losses': 0, 'difference': 0})

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    totals = [report['total'] for report in query]
    received = [(report['total'] - report["losses"]) for report in query]

    # Create the diagram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, totals, color='lightgray', label='Sent Packets', edgecolor='black', alpha=0.6)
    ax.fill_between(timestamps, received, color='steelblue', label='Received Packets', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Packets (Number of Packets)')
    ax.set_title('Temporal Distribution of Sent and Received UDP Packets')
    ax.legend(loc='upper left', frameon=False)

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if generate_png:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    plt.close()


def __plot_scenario_pps_over_time(test_scenario: tuple, output_path: str) -> None:
    diagram_name = 'pps_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3]

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    pps_sent = list()
    pps_received = list()

    for idx, report in enumerate(query):
        current_timestamp = report['timestamp']
        previous_timestamp = 0 if idx == 0 else query[idx-1]['timestamp']
        diff_timestamp = current_timestamp - previous_timestamp

        current_sent = report['total']
        previous_sent = 0 if idx == 0 else query[idx-1]['total']
        diff_total = current_sent - previous_sent
        pps_sent.append(diff_total / diff_timestamp)

        current_received = report['total'] - report['losses']
        previous_received = 0 if idx == 0 else (query[idx-1]['total'] - query[idx-1]['losses'])
        diff_received = current_received - previous_received
        pps_received.append(diff_received / diff_timestamp)

    # Create the diagram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, pps_sent, color='lightgray', label='Sent Packets', edgecolor='black', alpha=0.6)
    ax.fill_between(timestamps, pps_received, color='steelblue', label='Received Packets', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Packets (Number of Packets)')
    ax.set_title('Temporal Distribution of Sent and Received UDP Packets')
    ax.set_yscale('log')
    ax.legend(loc='upper left', frameon=False)

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if generate_png:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    plt.close()


def __plot_scenario_ppq_over_time(test_scenario: tuple, output_path: str) -> None:
    diagram_name = 'ppq_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3]

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    pps_sent = list()
    pps_received = list()

    for idx, report in enumerate(query):
        current_sent = report['total']
        previous_sent = 0 if idx == 0 else query[idx-1]['total']
        pps_sent.append(current_sent - previous_sent)

        current_received = report['total'] - report['losses']
        previous_received = 0 if idx == 0 else (query[idx-1]['total'] - query[idx-1]['losses'])
        pps_received.append(current_received - previous_received)

    # Create the diagram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, pps_sent, color='lightgray', label='Sent Packets', edgecolor='black', alpha=0.6)
    ax.fill_between(timestamps, pps_received, color='steelblue', label='Received Packets', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Packets (Number of Packets)')
    ax.set_title('Temporal Distribution of Sent and Received UDP Packets')
    ax.legend(loc='upper left', frameon=False)

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if generate_png:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    plt.close()
