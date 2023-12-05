import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Data
categories = ['80 Byte', '8900 Byte', '65000 Byte']
cpu_usr    = [3.1, 2.6, 0.7]
cpu_kernel = [25.5, 28.1, 27.2]
cpu_si     = [26, 22.8, 26.1]

# Set the style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
plt.rc('text', usetex=False)
plt.rc('font', family='serif')

fig, ax = plt.subplots(figsize=(12, 5))


# Stacked bar chart
#'colors' : {'datagramsize': {80: 'lightgray', 8900: 'steelblue', 65000: '#9fcc9f',},
ax.bar(categories, cpu_usr, label='user space', color='steelblue')
ax.bar(categories, cpu_kernel, bottom=cpu_usr, label='kernel space', color='lightgray')
ax.bar(categories, cpu_si, bottom=cpu_kernel, label='software interrupt handling', color='#9fcc9f')

# Labels, title, and other configurations
ax.set_ylabel('CPU time')
ax.set_xlabel('Datagram Size')
ax.set_title('CPU Usage by Test Scenario')
ax.legend(loc='upper right', frameon=True)
ax.set_ylim(0, 100)

def percent_formatter(x, _):
    return f"{x:.0f}%"
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
      

plt.savefig('ihawk_stern_cpu.png')
