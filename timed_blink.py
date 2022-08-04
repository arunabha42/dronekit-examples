import time
import argparse
from timeit import default_timer as timer
from distutils.util import strtobool

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--Button", help="Button state")

args = parser.parse_args()

btn = strtobool(args.Button)
print (f"Button state: {btn}")

def blink_led(duration):
    # Start timer, timer() returns the current time
    start = timer()

    # Blink at 1Hz for 25 secs
    while (timer()-start) < duration:        
        print(f"Time elapsed: {timer()-start}s")
        
        # Code to turn ON
        print("ON")
        time.sleep(1)
        # Code to turn OFF
        print("OFF")
        time.sleep(1)

def check_button_state(btn_state):

    if not btn_state:
        print("Button state false")    
        return False
    
    return True


#  Main program execution starts here
while True:
    if check_button_state(btn):
        # If button is pressed, blink LED for 25s
        blink_led(25)
        print("Exit while loop")
        break

    print("Button false, waiting for button input")