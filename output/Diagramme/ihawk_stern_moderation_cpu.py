import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Data
categories  = ['disabled', '62 µs', '84 µs', 'adaptive']
resu80b     = [54.7, 30.4, 29.2, 42.4]
resu8900b   = [53.5, 36  , 34.4, 30  ]
resu650000b = [54  , 34.4, 30.9, 26.1]

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



# Labels, title, and other configurations
ax.set_ylabel('CPU load')
ax.set_xlabel('Interrupt moderation setting')
ax.legend(loc='upper right', frameon=True, title='Datagram Size')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(categories)
ax.set_ylim(0, 100)

def percent_formatter(x, _):
    return f"{x:.0f}%"
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
      

plt.savefig('ihawk_stern_moderation_cpu.png')
