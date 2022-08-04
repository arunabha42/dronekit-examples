from imghdr import tests
import time
from tkinter import Button
from dronekit import connect
from pymavlink import mavutil

def set_servo_pwm(servo_instance, pwm_out):
    """ 
    Set an output on the servo rail.
    """
    
    global vehicle
    
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target_system, target_component
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
        0, #confirmation
        servo_instance-1,    # param 1, Servo instance number
        pwm_out,          # param 2, PWM in us
        0,          # param 3, not used
        0,          # param 4, not used
        0, 0, 0)    # param 5 ~ 7 not used

    # send command to vehicle
    vehicle.send_mavlink(msg)

def print_servoX_function(start, stop):
    '''
    Prints 
    '''
    for output in range(start, stop):
        param_name = f"SERVO{output}_FUNCTION"
        param_value = vehicle.parameters[param_name]
        print(f"{param_name} = {param_value}")

def set_params_original():
    print("\nSetting params back to original values..." )
    for output in range(1,9):
        vehicle.parameters[f"SERVO{output}_FUNCTION"] = servoX_functions_backup[output-1]

    print("\nParams after setting back to originals")
    print_servoX_function(1,9)

def backup_and_set_disabled():
    servoX_functions_backup = []
    servoX_trims_backup = []

    print("\nSetting VTOL outputs to Disabled..." )
    time.sleep(2)
    # Backup servo functions and modify VTOL outputs for MAVLink control
    for output in range(1,9):
        # Backup params for servo functions
        servoX_functions_backup.append(vehicle.parameters[f"SERVO{output}_FUNCTION"])
        servoX_trims_backup.append(vehicle.parameters[f"SERVO{output}_TRIM"])

        # For VTOL motors:
        # Set SERVOX_FUNCTION = Disabled so we can send DO_SET_SERVO commands
        # Set SERVOX_TRIM = 1000 as Disabled sets it to 1500 so it does not spin up
        if output in range(5,9):
            vehicle.parameters[f"SERVO{output}_FUNCTION"] = 0
            vehicle.parameters[f"SERVO{output}_TRIM"] = 1000


print("Connecting to vehicle...")
vehicle = connect("tcp:127.0.0.1:5762")
# vehicle = connect("tcp:100.125.149.27:14550")

# vehicle = connect("COM15")
print("Connected to vehicle")

# Set mode to manual
vehicle.mode ="MANUAL"
print("\nMode changed to Manual")
time.sleep(2)

# Set board safety to enable specific outputs
# vehicle.parameters["BRD_SAFETY_MASK"] = 1799
vehicle.parameters["BRD_SAFETY_MASK"] = int("0b11100000111", 2)

channels = [ "ROLL", "PITCH", "THROTTLE", "YAW"]

# Set CH 1-4
for input in [x for x in range(1,5) if x != 3]:
    if vehicle.mode != "MANUAL":
        vehicle.mode="MANUAL"

    print(f"\nTesting channel: {input}")
    
    # Get MIN & MAX for current RCIN channel
    rcin_max = int(vehicle.parameters[f"RC{input}_MAX"])
    rcin_min = int(vehicle.parameters[f"RC{input}_MIN"])

    # Set channel to MIN for 3s
    print(f"{channels[input-1]} - MIN")
    vehicle.channels.overrides[input] = rcin_min
    time.sleep(2)
    
    # Set channel to MAX for 3s
    print(f"{channels[input-1]} - MAX")
    vehicle.channels.overrides[input] = rcin_max
    time.sleep(2)

    # Clear all overrides
    vehicle.channels.overrides[input] = int(vehicle.parameters[f"RC{input}_TRIM"])
    time.sleep(2)


print("\nChanging mode to FBWA")
vehicle.mode = "FBWA"
time.sleep(1)

print("\nTesting rudder mixing")

print("ROLL MAX - Rudder Mix Check")
vehicle.channels.overrides[1] = int(vehicle.parameters["RC1_MAX"])
time.sleep(2)

print("ROLL MIN - Rudder Mix Check")
vehicle.channels.overrides[1] = int(vehicle.parameters["RC1_MIN"])
time.sleep(2)

# Clear all overrides
vehicle.channels.overrides[1] = int(vehicle.parameters[f"RC1_TRIM"])
time.sleep(1)

# Set board safety back to original
vehicle.parameters["BRD_SAFETY_MASK"] = 0

print("\nChanging mode to Manual")
vehicle.mode ="MANUAL"
