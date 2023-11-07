import time
from dronekit import connect
from pymavlink import mavutil

connection_string = "tcp:127.0.0.1:5762"

vehicle = connect(connection_string, wait_ready=True)

msg = vehicle.message_factory.winch_status_encode(
        0,       # time_boot_ms (not used)
        0,       # target num
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,       # frame
        10,
        12,
        0,       # altitude.  Not supported.
        0,0)     # size of target in radians

while True:
    vehicle.send_mavlink(msg)
    time.sleep(1)