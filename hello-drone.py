import time
from dronekit import connect

connection_string = "tcp:127.0.0.1:5762"
# connection_string = "com6"
# connection_string = "tcp:127.0.0.1:5770"
#connection_string = "udp:127.0.0.1:14550"

vehicle = connect(connection_string, wait_ready=True)

print(vehicle.gps_0)
print(vehicle.battery)
print(vehicle.last_heartbeat)
print(vehicle.is_armable)
print(vehicle.system_status.state)
print(vehicle.mode.name)

# Print location information for `vehicle` in all frames (default printer)
print ("Global Location: %s" % vehicle.location.global_frame)
print ("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print ("Local Location: %s" % vehicle.location.local_frame)    #NED

# Print altitudes in the different frames (see class definitions for other available information)
print ("Altitude (global frame): %s" % vehicle.location.global_frame.alt)
print ("Altitude (global relative frame): %s" % vehicle.location.global_relative_frame.alt)
print ("Altitude (NED frame): %s" % vehicle.location.local_frame.down)

# Create a message listener using the decorator.
# @vehicle.on_message('BATTERY_STATUS')
# def listener(self, name, message):
#     batt_watts = round(message.current_battery*message.voltages[0]/100000)
#     print(f"Current: {message.current_battery} A")
#     print(f"Voltage: {message.voltages[0]/1000} V")
#     print(f"Power: {batt_watts} W\n")

# #Create a message listener using the decorator.
@vehicle.on_message('STATUSTEXT')
def listener(self, name, message):
    # Filter out heartbeat packets from GCS
    # if message.autopilot != 8:
    if message.text == 'Land descend started':
        print("In landing stage, switching to QLAND")
        vehicle.mode = "QLAND"
    
# Create a message listener using the decorator.
# @vehicle.on_message('STATUSTEXT')
# def listener(self, name, message):
#     # Filter GCS STATUSTEXT messages

#     land_complete = 0
#     throttle_disarmed = 0

#     if message.text == 'Land complete':
#         print(message.text)
#         land_complete = 1

#     if message.text == 'Throttle disarmed':
#         print(message.text)
#         throttle_disarmed = 1

#     if land_complete and throttle_disarmed:
#         print("Ready for location check")

while True:
    time.sleep(2)

vehicle.close()