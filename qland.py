import time
from dronekit import connect

connection_string = "tcp:127.0.0.1:5762"

vehicle = connect(connection_string)
print("Connected to vehicle")

# #Create a message listener using the decorator.
@vehicle.on_message('STATUSTEXT')
def listener(self, name, message):
    # Filter out heartbeat packets from GCS
    # if message.autopilot != 8:
    if message.text == 'Land descend started':
        print("In landing stage, switching to QLAND")
        vehicle.mode = "QLAND"


while True:

    if vehicle.mode == 'QLAND':
        
        try:
            
            # Set RC overrides (channel values between 1000 and 2000)
            channel_values = [1300, 1500, 1500, 1500]
            
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
    
    time.sleep(1)