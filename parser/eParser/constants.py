import os

# FOLDER NAMES
output_folder = 'output'
results_folder = 'results'

# LOG NAMES
test_description_file = 'test_description.xml'
test_results_file = 'test_results.xml'

# TABLE OPTIONS
generate_excel = True
font_name = 'Arial'
monspace_font_name = 'Consolas'

# DIAGRAM OPTIONS
colors = {'datagramsize': {80: 'lightgray', 8900: 'steelblue', 65000: '#9fcc9f',},
          'paket_type': {'sent': 'lightgray', 'received': 'steelblue',},}
generate_histogram = False

generate_png = False
generate_latex = False


# EXECUTION OPTIONS
concurrent_execution = True