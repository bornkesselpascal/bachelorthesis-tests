import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Data
categories  = ['disabled', 'enabled', 'inverted']
resu80b     = [0, 0, 0]
resu8900b   = [0, 0, 0]
resu650000b = [0.00000756, 0.000005352, 0.000006364]


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
bar_width = 0.35

bar1 = ax.bar(index, resu80b, bar_width, label='80 Byte', color='lightgray')
bar2 = ax.bar(index + bar_width, resu8900b, bar_width, label='8900 Byte', color='steelblue')
bar3 = ax.bar(index + 2*bar_width, resu650000b, bar_width, label='65000 Byte', color='#9fcc9f')

for bar in bar1 + bar2 + bar3:
    height = bar.get_height()
    label = "{:.2e}%".format(height)
    ax.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

# Labels, title, and other configurations
ax.set_ylabel('Packet Loss (percentage)')
ax.set_xlabel('CPU Affinity')
ax.set_title('Packet Loss by Test Scenario for Direction R')
ax.legend(loc='upper right', frameon=True, title='Datagram Size')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(categories)
ax.set_yscale('log')

def percent_formatter(x, _):
    return f"{x:.0e}%"
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
      

plt.savefig('ihawk_stern_affinity_results.png')
