import os
from pymavlink import mavutil
from tabulate import tabulate

# Function to display parameters as a table
def display_parameters(parameters):
    table_data = []
    for param_name, param_value in parameters.items():
        table_data.append([param_name, param_value])
    print(tabulate(table_data, headers=["Parameter Name", "Value"], tablefmt="fancy_grid"))

# Function to search for a parameter and display the results as a table
def search_and_display(parameters, search_param):
    close_matches = [param_name for param_name in parameters.keys() if search_param.lower() in param_name.lower()]
    if close_matches:
        table_data = []
        for param_name in close_matches:
            table_data.append([param_name, parameters[param_name]])
        print(tabulate(table_data, headers=["Parameter Name", "Value"], tablefmt="fancy_grid"))
    else:
        print("No parameters found matching the search term.")

# Function to load parameters from the log file
def load_parameters_from_log(log_file_path):
    parameters = {}
    try:
        log_file = mavutil.mavlink_connection(log_file_path)
    except Exception as e:
        print(f"Error loading log file: {e}")
        return parameters

    while True:
        msg = log_file.recv_msg()
        if msg is None:
            break
        if msg.get_type() == 'PARM':
            param_name = msg.Name
            param_value = msg.Value
            parameters[param_name] = param_value

    return parameters

# Function to display the main menu
def display_menu():
    print("\nOptions:")
    print("1. Display all parameters")
    print("2. Search for a specific parameter")
    print("3. Exit")

# Open the .BIN log file
log_file_path = "log_test_AS04_ATOL.bin"

# Check if the log file exists
if not os.path.exists(log_file_path):
    print("Error: Log file not found.")
    exit()

# Get file size in a pretty format
file_size = os.path.getsize(log_file_path)
file_size_str = "{:.2f} MB".format(file_size / (1024 * 1024))
print(f"Log file size: {file_size_str}")

# Load parameters from the log file
parameters = load_parameters_from_log(log_file_path)

# Display total parameter count
total_parameters = len(parameters)
print(f"Total Parameters: {total_parameters}")

# Main loop
while True:
    display_menu()
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        display_parameters(parameters)
    elif choice == '2':
        search_param = input("Enter parameter name or part of it to search: ")
        search_and_display(parameters, search_param)
    elif choice == '3':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
