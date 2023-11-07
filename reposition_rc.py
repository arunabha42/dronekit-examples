import keyboard
import time
from dronekit import connect


def send_roll_pitch_overrides(vehicle, overrides):
    '''
    Receive list of roll, pitch PWM
    List of PWM in the format: overrides = [roll_pwm, pitch_pwm]
    Send as RC_OVERRIDE to aircraft
    '''

    for channel_num, value in enumerate(overrides, start=1):
        vehicle.channels.overrides[channel_num] = value
        print(f"Channel {channel_num}: {value}")

def run_repositioning(vehicle):
    '''
    Takes in a dronekit vehicle object and sends RC_OVERRIDE messages
    '''

    def keypressHandler(event):
        
        pwm_offset = 250

        if event.name == 'up':
            print("Arrow key pressed: UP")
            overrides = [1500, (1500 - pwm_offset)]
            send_roll_pitch_overrides(vehicle, overrides)
            
        if event.name == 'down':
            print("Arrow key pressed: DOWN")
            overrides = [1500, (1500 + pwm_offset)]
            send_roll_pitch_overrides(vehicle, overrides)
        
        if event.name == 'right':
            print("Arrow key pressed: RIGHT")
            overrides = [(1500 + pwm_offset), 1500]
            send_roll_pitch_overrides(vehicle, overrides)
        
        if event.name == 'left':
            print("Arrow key pressed: LEFT")
            overrides = [(1500 - pwm_offset), 1500]
            send_roll_pitch_overrides(vehicle, overrides)
        

    keyboard.on_press(keypressHandler)

    while True:
        
        time.sleep(0.5)