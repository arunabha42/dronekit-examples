from dronekit import connect, VehicleMode
import time

# Set your connection string (e.g., "udp:127.0.0.1:14550" for a local UDP connection

def offsetCorrection(pidx,pidy,vehicle):
            # Apply min-max scaling to make x and y values zero-centered
            x_min = -999
            x_max = 999
            y_min = -999
            y_max = 999

            x_scaled = (pidx - x_min) / (x_max - x_min) * (2000 - 1000)
            y_scaled = (pidy - y_min) / (y_max - y_min) * (2000 - 1000)

            # Ensure scaled values are within the valid RC input range (1000 - 2000)
            rc_channel1 = max(1000, min(2000, 1500 + int(x_scaled)))  # Channel 1 (Roll)
            rc_channel2 = max(1000, min(2000, 1500 + int(y_scaled)))  # Channel 2 (Pitch)

            # Send RC override messages
            vehicle.channels.overrides[1] = rc_channel1
            vehicle.channels.overrides[2] = rc_channel2
            time.sleep(0.05)
            vehicle.channels.overrides[1] = 1500
            vehicle.channels.overrides[2] = 1500

            print("RC Overrides - Channel 1:", rc_channel1, "Channel 2:", rc_channel2)


        # Sleep for a while before generating the next message
            time.sleep(0.175)
def resetQuit(vehicle):
        vehicle.channels.overrides[1] = 1500
        vehicle.channels.overrides[2] = 1500
        vehicle.close()
        quit()
        
