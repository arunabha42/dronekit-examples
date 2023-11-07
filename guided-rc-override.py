from dronekit import connect, VehicleMode
import time
# Set your connection string (e.g., "udp:127.0.0.1:14550" for a local UDP connection)
connection_string = "tcp:127.0.0.1:5762"
# Connect to the vehicle
vehicle = connect(connection_string)
try:
    # Arm the vehicle
    # vehicle.mode = VehicleMode("QLAND")
    # vehicle.armed = True
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)
    # Set RC overrides (channel values between 1000 and 2000)
    channel_values = [2000, 1500, 1500, 1500]
    # Send RC overrides for channels 1 to 8
    for channel_num, value in enumerate(channel_values, start=1):
        vehicle.channels.overrides[channel_num] = value
        print(f"Channel {channel_num}: {value}")
    # Wait for a few seconds to apply the overrides
    time.sleep(5)
    # Clear RC overrides
    vehicle.channels.overrides = {}
    print("RC overrides cleared.")
finally:
    # Disarm and close the connection
    # vehicle.armed = False
    vehicle.close()