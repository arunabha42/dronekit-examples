import keyboard
import time

def keypressHandler(event):
    
    if event.name == 'up':
        print("Arrow key pressed: UP")
        
    if event.name == 'down':
        print("Arrow key pressed: DOWN")
    
    if event.name == 'right':
        print("Arrow key pressed: RIGHT")
    
    if event.name == 'left':
        print("Arrow key pressed: LEFT")
    

keyboard.on_press(keypressHandler)

while True:

    print(f"{overrides}")
    time.sleep(0.5)