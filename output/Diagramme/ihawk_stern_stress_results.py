import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Data
categories  = ['80 Byte', '8900 Byte', '65000 Byte']
direction_h = [0, 0, 0.00087491043108970500]
direction_r = [0, 0, 0.000017461187436265]


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

bar1 = ax.bar(index, direction_h, bar_width, label='H', color='lightgray')
bar2 = ax.bar(index + bar_width, direction_r, bar_width, label='R', color='steelblue')

for bar in bar1 + bar2:
    height = bar.get_height()
    label = "{:.2e}%".format(height)
    ax.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

# Labels, title, and other configurations
ax.set_ylabel('Packet Loss (percentage)')
ax.set_xlabel('Datagram Size')
ax.set_title('Packet Loss by Test Scenario')
ax.legend(loc='upper right', frameon=True, title='Direction')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(categories)
ax.set_yscale('log')

def percent_formatter(x, _):
    return f"{x:.0e}%"
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
      

plt.savefig('ihawk_stern_stress_results.png')
