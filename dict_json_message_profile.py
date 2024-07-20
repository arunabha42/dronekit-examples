import time
import sys
from dronekit import connect

# Connection strings
connection_string_sitl_local = "tcp:127.0.0.1:5762"

CONNECTION_STRING = connection_string_sitl_local
PROFILE_DURATION = 5

vehicle = connect(CONNECTION_STRING, wait_ready=False)

message_list = ['AHRS2',
                'AUTOPILOT_VERSION',
                'BATTERY_STATUS',
                'EKF_STATUS_REPORT',
                'GLOBAL_POSITION_INT',
                'GPS_RAW_INT',
                'HEARTBEAT',
                'HOME_POSITION',
                'POWER_STATUS',
                'TERRAIN_REPORT',
                'VFR_HUD',
                'VIBRATION',
                'WIND'
                ]

message_data = {
    message_type: {
        'sizes': [],
        'dict_sizes': [],
        'json_sizes': [],
        'dict_changes': [],
        'json_changes': [],
        'dict_change_percent': [],
        'json_change_percent': [],
        'count': 0
    } for message_type in message_list
}


# Create a message listener using the decorator.
@vehicle.on_message(message_list)
def listener(self, name, message):
    # Get sizes of message, dict, and JSON
    message_size = sys.getsizeof(message)
    dict_size = sys.getsizeof(message.to_dict())
    json_size = sys.getsizeof(message.to_json())

    # Add to message_data profile
    message_data[message.get_type()]['sizes'].append(message_size)
    message_data[message.get_type()]['dict_sizes'].append(dict_size)
    message_data[message.get_type()]['json_sizes'].append(json_size)
    message_data[message.get_type()]['count'] += 1

    # Calculate size changes
    dict_change = dict_size - message_size
    json_change = json_size - message_size
    message_data[message.get_type()]['dict_changes'].append(dict_change)
    message_data[message.get_type()]['json_changes'].append(json_change)
    message_data[message.get_type()]['dict_change_percent'].append((dict_change / message_size) * 100)
    message_data[message.get_type()]['json_change_percent'].append((json_change / message_size) * 100)

def print_results(message_data):
    print(f"\nPROFILE RESULTS")
    print("----------------------\n")
    
    for message_type, data in message_data.items():
        if data['sizes']:
            sum_size = sum(data['sizes'])
            avg_size = sum(data['sizes']) / len(data['sizes'])
            min_size = min(data['sizes'])
            max_size = max(data['sizes'])
            count = data['count']
            
            sum_dict_size = sum(data['dict_sizes'])
            avg_dict_size = sum(data['dict_sizes']) / len(data['dict_sizes'])
            min_dict_size = min(data['dict_sizes'])
            max_dict_size = max(data['dict_sizes'])
            
            sum_json_size = sum(data['json_sizes'])
            avg_json_size = sum(data['json_sizes']) / len(data['json_sizes'])
            min_json_size = min(data['json_sizes'])
            max_json_size = max(data['json_sizes'])
            
            avg_dict_change = sum(data['dict_changes']) / len(data['dict_changes'])
            avg_json_change = sum(data['json_changes']) / len(data['json_changes'])
            avg_dict_change_percent = sum(data['dict_change_percent']) / len(data['dict_change_percent'])
            avg_json_change_percent = sum(data['json_change_percent']) / len(data['json_change_percent'])
            
            # print("----------------------")
            # print({message_type})
            # print("----------------------")

            # print(f"Count:\t\t{count}")                
            # print(f"Rate:\t\t{round(count / PROFILE_DURATION,1)} Hz")
            # print(f"Sum:\t\t{round(sum_size)} bytes")
            # print(f"Average:\t{round(avg_size)} bytes")
            
            # if min_size != max_size:
            #     print(f"Min:\t\t{round(min_size)} bytes")
            #     print(f"Max:\t\t{round(max_size)} bytes\n")
                
            # print(f"Sum (Dict):\t\t{round(sum_dict_size)} bytes")
            # print(f"Average (Dict):\t{round(avg_dict_size)} bytes")
            # print(f"Min (Dict):\t\t{round(min_dict_size)} bytes")
            # print(f"Max (Dict):\t\t{round(max_dict_size)} bytes\n")
            
            # print(f"Sum (JSON):\t\t{round(sum_json_size)} bytes")
            # print(f"Average (JSON):\t{round(avg_json_size)} bytes")
            # print(f"Min (JSON):\t\t{round(min_json_size)} bytes")
            # print(f"Max (JSON):\t\t{round(max_json_size)} bytes\n")
            
            # print(f"Average Change (Dict):\t\t{round(avg_dict_change)} bytes")
            # print(f"Average Change (JSON):\t\t{round(avg_json_change)} bytes")
            # print(f"Average Change (Dict %):\t{round(avg_dict_change_percent)} %")
            # print(f"Average Change (JSON %):\t{round(avg_json_change_percent)} %")

    total_message_count = sum(data['count'] for data in message_data.values())
    total_message_types = len(message_data)
    total_size = sum(sum(data['sizes']) for data in message_data.values())
    avg_total = total_size / total_message_count

    total_dict_size = sum(sum(data['dict_sizes']) for data in message_data.values())
    total_json_size = sum(sum(data['json_sizes']) for data in message_data.values())

    total_dict_change = sum(sum(data['dict_changes']) for data in message_data.values())
    total_json_change = sum(sum(data['json_changes']) for data in message_data.values())

    avg_dict_change = total_dict_change / total_message_count
    avg_json_change = total_json_change / total_message_count

    avg_dict_change_percent = sum(sum(data['dict_change_percent']) for data in message_data.values()) / total_message_count
    avg_json_change_percent = sum(sum(data['json_change_percent']) for data in message_data.values()) / total_message_count

    ratio_dict_change = avg_dict_change / avg_total
    ratio_json_change = avg_json_change / avg_total

    print("\n----------------------")
    print(f"PROFILE SUMMARY")
    print("----------------------")
    print(f"Duration of profiling run:\t{PROFILE_DURATION} seconds")
    print(f"Total messages received:\t{total_message_count}")
    print(f"Average message rate:\t\t{round(total_message_count/PROFILE_DURATION)} messages/second")
    print(f"Total Message Types: \t\t{total_message_types}")
    print(f"Total size:\t\t\t{round(total_size)} bytes")
    print(f"Average message size:\t\t{round(avg_total)} bytes")
    print(f"Average data rate:\t\t{round(total_size/PROFILE_DURATION)} bytes/second")
    print(f"Total Dict size:\t\t{round(total_dict_size)} bytes")
    print(f"Total JSON size:\t\t{round(total_json_size)} bytes")
    print(f"Average Change (Dict):\t\t{round(avg_dict_change)} bytes")
    print(f"Average Change (JSON):\t\t{round(avg_json_change)} bytes")
    print(f"Average Change (Dict %):\t{round(avg_dict_change_percent)} %")
    print(f"Average Change (JSON %):\t{round(avg_json_change_percent)} %")
    print(f"Raw Message : Dict : JSON\t1 : {round(ratio_dict_change, 1)} : {round(ratio_json_change, 1)}")
    print("----------------------\n")


# Run the profile
print("Starting profile...")
start_time = time.time()    
while time.time() - start_time < PROFILE_DURATION:
    time.sleep(1)

print_results(message_data)