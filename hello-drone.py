import time
from dronekit import connect

connection_string = "tcp:127.0.0.1:5762"

vehicle = connect(connection_string, wait_ready=True)

print(vehicle.gps_0)
print(vehicle.battery)
print(vehicle.last_heartbeat)
print(vehicle.is_armable)
print(vehicle.system_status.state)
print(vehicle.mode.name)

#Create a message listener using the decorator.
@vehicle.on_message('BATTERY_STATUS')
def listener(self, name, message):
    batt_watts = round(message.current_battery*message.voltages[0]/100000)
    print(f"Power: {batt_watts} W")

# #Create a message listener using the decorator.
# @vehicle.on_message('HEARTBEAT')
# def listener(self, name, message):
#     # Filter out heartbeat packets from GCS
#     if message.autopilot != 8:
#         print(message)

while True:
    time.sleep(2)

vehicle.close()