import time
import sys

from dronekit import connect

# Connection strings
connection_string_sitl_local = "tcp:127.0.0.1:5762"
CONNECTION_STRING = connection_string_sitl_local

vehicle = connect(CONNECTION_STRING, wait_ready=False)


message_list = ['VFR_HUD', 'GPS_RAW_INT', 'GLOBAL_POSITION_INT', 'BATTERY_STATUS']
message_data = {message_type: {'sizes': [], 'count': 0} for message_type in message_list}

PROFILE_DURATION = 120

# Create a message listener using the decorator.
@vehicle.on_message(message_list)
def listener(self, name, message):
    # print(f"Received: {message.get_type()}\t{sys.getsizeof(message)} bytes")
    
    # Add to message_data profile
    message_data[message.get_type()]['sizes'].append(sys.getsizeof(message))
    message_data[message.get_type()]['count'] += 1
    

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
                print("----------------------")
                print({message_type})
                print("----------------------")

                print(f"Count:\t\t{count}")                
                print(f"Rate:\t\t{round(count / PROFILE_DURATION,1)} Hz")
                print(f"Sum:\t\t{sum_size} bytes")
                print(f"Average:\t{round(avg_size)} bytes")
                
                if min_size != max_size:
                    print(f"Min:\t\t{min_size} bytes")
                    print(f"Max:\t\t{max_size} bytes\n")

        total_message_count = sum(data['count'] for data in message_data.values())
        total_message_types = len(message_data)
        total_size = sum(sum(data['sizes']) for data in message_data.values())
        avg_total = total_size / total_message_count

        print("\n----------------------")
        print(f"PROFILE SUMMARY")
        print("----------------------")
        print(f"Duration of profiling run:\t{PROFILE_DURATION} seconds")
        print(f"Total messages received:\t{total_message_count}")
        print(f"Average message rate:\t\t{round(total_message_count/PROFILE_DURATION)} messages/second")
        print(f"Total Message Types: \t\t{total_message_types}")
        print(f"Total size:\t\t\t{total_size} bytes")
        print(f"Average message size:\t\t{round(avg_total)} bytes")
        print(f"Average data rate:\t\t{round(total_size/PROFILE_DURATION)} bytes/second")
        print("----------------------\n")

# Run the profile
print("Starting profile...")
start_time = time.time()    
while time.time() - start_time < PROFILE_DURATION:
    time.sleep(0.1)

print_results(message_data)