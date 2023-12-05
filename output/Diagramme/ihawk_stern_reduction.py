import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Data
categories = ['8 Links', '7 Links', '6 Links', '5 Links']
cpu_usr    = [0.000018563058, 0.000013504, 0.0000015460247, 0]


# Set the style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
plt.rc('text', usetex=False)
plt.rc('font', family='serif')

fig, ax = plt.subplots(figsize=(12, 5))


# Stacked bar chart
#'colors' : {'datagramsize': {80: 'lightgray', 8900: 'steelblue', 65000: '#9fcc9f',},
bar = ax.bar(categories, cpu_usr, label='user space', color='steelblue')

for bar in bar:
    height = bar.get_height()
    label = "{:.3e}%".format(height)
    ax.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

# Labels, title, and other configurations
ax.set_ylabel('Packet Loss (ratio)')
ax.set_xlabel('Number of bidirectional Links')
ax.set_title('Packet Loss by Number of utilized Links in Direction R')

def percent_formatter(x, _):
    return f"{x:.0e}%"
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
      

plt.savefig('ihawk_stern_reduction.png')
