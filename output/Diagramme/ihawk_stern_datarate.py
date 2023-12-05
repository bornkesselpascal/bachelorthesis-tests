import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Data
categories  = ['Center', 'Endpoint 1', 'Endpoint 2', 'Endpoint 3', 'Endpoint 4']
resu80b     = [64.12456, 98.376, 69.87968, 76.78752, 94.29696]
resu8900b   = [5696.8277, 7439.7948, 6614.48, 6873.3632, 7224.87760]
resu650000b = [9896.25, 8499.9, 8178.6, 8106.8, 8305.2]




# Set the style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
plt.rc('text', usetex=False)
plt.rc('font', family='serif')

fig, ax = plt.subplots(figsize=(12, 5))


# Stacked bar chart
#'colors' : {'datagramsize': {80: 'lightgray', 8900: 'steelblue', 65000: '#9fcc9f',},
n_groups = len(categories)
index = np.arange(n_groups)
bar_width = 0.2

bar1 = ax.bar(index, resu80b, bar_width, label='80 Byte', color='lightgray')
bar2 = ax.bar(index + bar_width, resu8900b, bar_width, label='8900 Byte', color='steelblue')
bar3 = ax.bar(index + 2*bar_width, resu650000b, bar_width, label='65000 Byte', color='#9fcc9f')

for bar in bar1 + bar2 + bar3:
    height = bar.get_height()
    label = "{:.0f} Mbit/s".format(height)
    ax.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')


# Labels, title, and other configurations
ax.set_ylabel('Datenübertragungsrate')
ax.set_xlabel('System')
ax.legend(loc='upper right', frameon=True, title='Datagram Size')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(categories)
ax.set_yscale('log')

def percent_formatter(x, _):
    return f"{x:.0f} Mbps"
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
      

plt.savefig('ihawk_stern_datarate.png')
