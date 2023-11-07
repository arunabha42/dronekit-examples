from dronekit import connect, VehicleMode
import time
# Set your connection string (e.g., "udp:127.0.0.1:14550" for a local UDP connection)
# connection_string = "udp:127.0.0.1:14881"
connection_string = "udpin:127.0.0.1:14882"
# connection_string = "tcp:10.42.0.1:5760"
# connection_string = "udp:10.42.0.26:14890"
# Connect to the vehicle
vehicle = connect(connection_string, wait_ready=True)

print(vehicle.gps_0)
vehicle.mode = "GUIDED"
vehicle.mode = "Stabilize"

vehicle.close()