import os
from constants import test_description_file, test_results_file

def validate_test_folder(path) -> bool:
    files_in_path = os.listdir(path)
    return test_description_file in files_in_path and test_results_file in files_in_path

def check_server_data(server_folder, test_folder) -> bool:
    test_folder_server = os.path.join(server_folder, test_folder)
    if not os.path.exists(test_folder_server):
        return False
    
    return validate_test_folder(test_folder_server)
    