from dronekit import connect
import time 
from datetime import datetime

connection_string = "tcp:127.0.0.1:5762"

vehicle = connect(connection_string)
print("Connected to vehicle")

# #Create a message listener using the decorator.
@vehicle.on_message('GPS_RAW_INT')
def listener(self, name, message):
    
    gps_dt = datetime.fromtimestamp(message.time_usec)
    print(f"GPS UNIX timestamp: \t{message.time_usec}")
    print(f"Date & time: \t\t{gps_dt}")
    print(f"Timezone: \t\t{gps_dt.tzinfo}\n")

# #Create a message listener using the decorator.
@vehicle.on_message('SYSTEM_TIME')
def listener(self, name, message):
    
    sys_dt = datetime.fromtimestamp(message.time_unix_usec/1000000)
    print(f"System UNIX timestamp: \t{message.time_unix_usec}")
    print(f"Date & time: \t\t{sys_dt}")
    print(f"Timezone: \t\t{sys_dt.tzinfo}\n")


# while True:
#     time.sleep(1)

for i in range(1):
    time.sleep(1)

vehicle.close()