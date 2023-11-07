import time
from dronekit import connect

connection_string = "tcp:127.0.0.1:5763"

vehicle = connect(connection_string)
print("Connected to vehicle")

# #Create a message listener using the decorator.
@vehicle.on_message('STATUSTEXT')
def listener(self, name, message):
        
    if message.text == 'Land complete':
        print("Received message: Land complete")
    
    if message.text == 'Throttle disarmed':
        print("Received message: Throttle disarmed")

while True:
    time.sleep(1)