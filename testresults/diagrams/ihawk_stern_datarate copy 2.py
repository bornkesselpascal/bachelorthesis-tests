import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Data
categories  = ['enabled', 'inverted']
resu        = [9672.455, 9406.475]




# Set the style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
plt.rc('text', usetex=False)
plt.rc('font', family='serif')

fig, ax = plt.subplots(figsize=(4, 5))


# Stacked bar chart
#'colors' : {'datagramsize': {80: 'lightgray', 8900: 'steelblue', 65000: '#9fcc9f',},
bar1 = ax.bar(categories, resu, label='80 Byte', color='#9fcc9f')

for bar in bar1:
    height = bar.get_height()
    label = "{:.0f} Mbit/s".format(height)
    ax.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')


# Labels, title, and other configurations
ax.set_ylabel('Datenübertragungsrate (Mbit/s)')
ax.set_xlabel('CPU affinity')
ax.set_title('65000 Byte')

def percent_formatter(x, _):
    return f"{x:.0f} Mbit/s"
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
      

plt.savefig('ihawk_stern_datarate.png')
