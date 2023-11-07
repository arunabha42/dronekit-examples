from dronekit import connect
import time

conenction_string = 'tcp:127.0.0.1:5762'
vehicle = connect(conenction_string, wait_ready=True)

land_complete = 0
throttle_disarmed = 0

# Create a message listener using the decorator.
@vehicle.on_message('STATUSTEXT')
def listener(self, name, message):
    # Filter GCS STATUSTEXT messages

    global land_complete
    global throttle_disarmed

    print(message.text)

    if message.text == 'Land complete':
        # print(message.text)
        land_complete = 1

    if message.text == 'Throttle disarmed':
        # print(message.text)
        throttle_disarmed = 1

    if land_complete and throttle_disarmed:
        print("Ready for location check")



while not land_complete and not throttle_disarmed:
    print("Waiting for land complete and throttle disarm...")
    time.sleep(1)

print("Land complete & throttle disarmed")
print("TODO: Switch safety ON")

vehicle.close()