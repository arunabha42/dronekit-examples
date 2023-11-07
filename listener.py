import time
from dronekit import connect

connection_string = "tcp:127.0.0.1:5762"

vehicle = connect(connection_string)

# #Create a message listener using the decorator.
@vehicle.on_message('GPS_RAW_INT')
def listener(self, name, message):
    print(type(message))

while True:
    print(f"From Dronekit:\n{type(vehicle.gps_0)}")
    time.sleep(0.1)