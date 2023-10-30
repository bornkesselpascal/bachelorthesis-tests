import os

# FOLDER NAMES
results_folder = 'results_demo'
client_folder = os.path.join(results_folder, 'client')
server_folder = os.path.join(results_folder, 'server')
output_folder = 'output'

# LOG NAMES
test_description_file = 'test_description.xml'
test_results_file = 'test_results.xml'

# TABLE OPTIONS
generate_excel = True

# DIAGRAM OPTIONS
colors = {80: 'lightgray', 8900: 'steelblue', 65000: '#9fcc9f'}
generate_histogram = False

generate_png = False
generate_latex = False


# EXECUTION OPTIONS
concurrent_execution = True