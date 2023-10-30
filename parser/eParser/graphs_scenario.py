import os
import seaborn as sns
import matplotlib.pyplot as plt
from constants import generate_latex, generate_png, generate_histogram
from data_format import format_query


#                                _                               _
#                               (_)                             | |
#  ___  ___ ___ _ __   __ _ _ __ _  ___     __ _ _ __ __ _ _ __ | |__  ___
# / __|/ __/ _ \ '_ \ / _` | '__| |/ _ \   / _` | '__/ _` | '_ \| '_ \/ __|
# \__ \ (_|  __/ | | | (_| | |  | | (_) | | (_| | | | (_| | |_) | | | \__ \
# |___/\___\___|_| |_|\__,_|_|  |_|\___/   \__, |_|  \__,_| .__/|_| |_|___/
#                                           __/ |         | |
#                                          |___/          |_|


def _prepare_and_create_scenario_graphs(test_scenario: tuple, output_path: str) -> None:
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
