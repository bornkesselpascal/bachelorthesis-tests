import os
import math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
from constants import generate_latex, generate_png, colors


#                                  _                                     _
#                                 (_)                                   | |
#   ___ __ _ _ __ ___  _ __   __ _ _  __ _ _ __     __ _ _ __ __ _ _ __ | |__  ___
#  / __/ _` | '_ ` _ \| '_ \ / _` | |/ _` | '_ \   / _` | '__/ _` | '_ \| '_ \/ __|
# | (_| (_| | | | | | | |_) | (_| | | (_| | | | | | (_| | | | (_| | |_) | | | \__ \
#  \___\__,_|_| |_| |_| .__/ \__,_|_|\__, |_| |_|  \__, |_|  \__,_| .__/|_| |_|___/
#                     | |             __/ |         __/ |         | |
#                     |_|            |___/         |___/          |_|


def _prepare_and_create_campaign_graphs(test_data: list, campaign_folder: str) -> None:
    __plot_campaign_diagr1(test_data, campaign_folder)
    __plot_campaign_diagr2(test_data, campaign_folder)


def __plot_campaign_diagr1(test_data: list, output_path: str) -> None:
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
    index = np.arange(len(x_labels))

    _, ax = plt.subplots(figsize=(12, 5))
    for idx, (size, values) in enumerate(sorted_losses_per_size.items()):
        ax.bar(index + bar_width * idx, values, bar_width, color=colors['datagramsize'].get(size, 'red'), edgecolor='black', label=f"{size} Byte", alpha=0.7)

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
    index = np.arange(len(cycle_times))

    bars = list()
    _, ax = plt.subplots(figsize=(12, 5))
    for idx, (size, values) in enumerate(sorted_losses_per_size.items()):
        bars.append(ax.bar(index + bar_width * idx, values, bar_width, color=colors['datagramsize'].get(size, 'red'), edgecolor='black', label=f"{size} Byte", alpha=0.7))

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
