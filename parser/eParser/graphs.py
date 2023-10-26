import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import os
import seaborn as sns
from constants import generate_latex
from data_format import *

def plot_campaign_loss_per_datagram_size(test_data: list, output_path: str) -> None:
    diagram_name = 'loss_per_datagram_size'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')
    
    # Fetch the data for the visualization
    x_labels = ['0', ']0;10]', ']10;20]', ']20;30]', ']30;40]', ']40;50]', ']50;60]', ']60;70]', ']70;80]', ']80;90]', ']90;100]']
    losses_per_size = dict(list())

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

    sorted_losses_per_size = {k: losses_per_size[k] for k in sorted(losses_per_size, reverse=True)}


    # Create a bar chart for each datagram size
    barWidth = 0.55                                         # width of the bars
    colors = ['lightgray', 'steelblue', '#9fcc9f', '#ffb3e6']   # colors for the bars

    r = np.arange(len(x_labels))
    bottom_values = np.zeros(len(x_labels))

    fig, ax = plt.subplots(figsize=(12, 5))
    for idx, (size, values) in enumerate(sorted_losses_per_size.items()):
        ax.bar(r, values, bottom=bottom_values, color=colors[idx % len(colors)], edgecolor='black', width=barWidth, label=f"{size} Byte", alpha=0.7)
        bottom_values = [i+j for i,j in zip(bottom_values, values)]


    # Add axis labels and titles
    ax.set_xlabel('Packet Losses (Percentage)')
    ax.set_ylabel('Test Cases (Number of Test Cases)')
    ax.set_title('Packet Loss Ratio of all Test Cases (across all Datagram Sizes and Cycle Times)')
    ax.set_xticks(r, x_labels)
    ax.legend(loc='upper left', frameon=False)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    
    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    #plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)
    plt.close()


def plot_campaign_loss_per_cycle_time(test_data: list, output_path: str) -> None:
    diagram_name = 'loss_per_cycle_time'
    pass



def plot_scenario_histogram_losses(test_scenario: tuple((dict, dict, dict, list)), output_path: str) -> None:
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
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.hist(differences_list, bins=range(0, max(differences_list) + 2), align='left', color='steelblue', edgecolor='black', alpha=0.7)

    # Labels, title, and other configurations
    ax.set_xlabel('Packet Losses per 100000 Packets (Number of Packets)')
    ax.set_ylabel('Frequency')
    #ax.set_yscale('log')
    ax.set_title('Frequency Analysis of Packet Losses')
    ax.set_xticks(range(0, max(differences_list) + 10, 10))
    plt.tight_layout()

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    
    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    #plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)
    plt.close()


def plot_scenario_losses_over_time(test_scenario: tuple((dict, dict, dict, list)), output_path: str) -> None:
    diagram_name = 'losses_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3]
    query.insert(0, {'timestamp': 0, 'total': 0, 'losses': 0, 'difference': 0})

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    difference = [report['difference'] for report in query]

    # Create the diagram
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, difference, color='lightgray', edgecolor='black', alpha=0.6)
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Lost Packets (Number of Packets)')
    #ax.set_yscale('log')
    ax.set_title('Temporal Distribution of Packet Loss')

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    
    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    #plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)
    plt.close()


def plot_scenario_packages_over_time(test_scenario: tuple((dict, dict, dict, list)), output_path: str) -> None:
    diagram_name = 'packages_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3]
    query.insert(0, {'timestamp': 0, 'total': 0, 'losses': 0, 'difference': 0})

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    totals = [report['total'] for report in query]
    received = [(report['total'] - report["losses"]) for report in query]

    # Create the diagram
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, totals, color='lightgray', label='Sent Packets', edgecolor='black', alpha=0.6)
    ax.fill_between(timestamps, received, color='steelblue', label='Received Packets', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Packets (Number of Packets)')
    ax.set_title('Temporal Distribution of Sent and Received UDP Packets')
    ax.legend(loc='upper left', frameon=False)

    # Save the diagram
    if generate_latex:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    
    plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    #plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)
    plt.close()