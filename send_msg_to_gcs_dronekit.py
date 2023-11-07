from dronekit import connect
from pymavlink import mavutil
import time

vehicle = connect('tcp:127.0.0.1:5762', source_system=232, wait_ready=True)
# vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)

while True:
    text_binary = 'Printing from Dronekit'.encode()
    print(type(text_binary))

    msg = vehicle.message_factory.statustext_encode(
        mavutil.mavlink.MAV_SEVERITY_ALERT,  #severity
        text_binary # binary encoded text
    )

    vehicle.send_mavlink(msg)

    time.sleep(1)