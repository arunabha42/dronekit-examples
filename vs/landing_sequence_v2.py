from dronekit import connect, VehicleMode
from pymavlink import mavutil
import threading
import moveBool
import time
import planeoverride_v2_1

connection_string = 'tcp:192.168.0.123:5762'  # Change to your connection string
the_connection = connect(connection_string)
# Desired GPS coordinates (latitude and longitude) for reaching the location
#desired_latitude =-35.3627141
# Replace with your desired latitude
#desired_longitude = 149.1651160
# Replace with your desired longitude
#desired altitude to switch to guided mode
#desiredalt=30
#safealt=6.5
#descentrate = 1.1
#checksum = modeoutput.listener(the_connection)
global throttle_flag
throttle_flag = False

# Connect to the autopilot
@the_connection.on_message('STATUSTEXT')
def listener(self, name, message):
    # Filter out heartbeat packets from GCS
    # if message.autopilot != 8:
    if message.text == 'Land descend started':
        print("In landing stage, switching to QLAND")
        the_connection.mode = "QLAND"
    if message.text == "Throttle disarmed":
        throttle_flag = True

while True:

    if the_connection.mode == 'QLAND':
        if throttle_flag:
            planeoverride_v2_1.resetQuit(the_connection)
        else:
            moveBool.control_drone(the_connection)
            time.sleep(0.15)
    