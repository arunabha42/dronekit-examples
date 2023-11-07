import time
from dronekit import connect

import reposition_rc

connection_string = "tcp:127.0.0.1:5762"

vehicle = connect(connection_string)
print("Connected to vehicle")

# --------- FUNCTIONS ----------

def wait_for_landing_stage(vehicle):
    
    print("Waiting for landing stage...")
    in_landing_stage = False

    # Listen for landing stage message
    @vehicle.on_message('STATUSTEXT')
    def handle_status_text(self, name, msg):
        print(msg.text)
        if msg.text == "Land descend started":
             nonlocal in_landing_stage
             in_landing_stage = True
             print("In landing stage, looking for ArUco marker")

    while not in_landing_stage:
        pass

    return in_landing_stage

def detect_first_aruco(vehicle):

    aruco_detected = True

    while not aruco_detected:
        print("Waiting for ArUco...")
        time.sleep(1)
        
    print("First detection of ArUco marker")
    print("Setting modeto QLAND")
    vehicle.mode = 'QLAND'
    return aruco_detected
        
def dummy_run_repositioning():

    reposition_required = False

    while reposition_required:
        print("Repositioning...")
        time.sleep(1)

    else:
        return




# --------- MAIN SEQUENCE -------------
wait_for_landing_stage(vehicle)

# Wait for first detection of marker, only then switch to QLAND
# If ArUco is never detected, continue in AUTO
detect_first_aruco(vehicle)

# Run repositioning code over marker
reposition_rc.run_repositioning(vehicle)

# Close connection & exit program
vehicle.close()
