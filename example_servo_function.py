import time
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

print("Connecting to vehicle...")
vehicle = connect("tcp:127.0.0.1:5762")
print("Connected to vehicle")

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

# TODO:

print("\nChanged values")
print_servoX_function(1,9)