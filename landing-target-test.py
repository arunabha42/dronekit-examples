from dronekit import connect
from pymavlink import mavutil
import time


def send_land_message(vehicle, x,y,z):
    msg = vehicle.message_factory.landing_target_encode(
        0,          # time since system boot, not used
        0,          # target num, not used
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame, not used
        #(x-horizontal_resolution/2)*horizontal_fov/horizontal_resolution,
        x, # only for test
        #(y-vertical_resolution/2)*vertical_fov/vertical_resolution,
        y, # only for test
        z,          # distance, in meters
        0,          # Target x-axis size, in radians
        0           # Target y-axis size, in radians
    )


    vehicle.send_mavlink(msg)
    vehicle.flush()


vehicle = connect('tcp:127.0.0.1:5762', source_system=1)

x = 0
y = 0
z = 0

while True:
    send_land_message(vehicle, x, y, z)
    time.sleep(1)