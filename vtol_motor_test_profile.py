import time
import sys

from dronekit import connect
from pymavlink import mavutil

'''
1. Connect to vehicle
2. Ramp up motors to 80%
3. Maintain throttle at 60% for 60 seconds
'''

# --------------------------------------
# USER PARAMS
# --------------------------------------
CONNECTION_STRING = "tcp:127.0.0.1:5770"

VTOL_MOTOR_CHANNELS = range(5,9)

# Test profile parameters
PWM_ESC = {
            "min":      1000,
            "max":      2000
        }

TEST_PROFILE = {
                "spool":    { "pct": 0.12, "time": 3 },
                "peak":     { "pct": 0.70, "time": 3 },
                "hover":    { "pct": 0.65, "time": 5 }
            }

# --------------------------------------
# FUNCTION DEFINITIONS
# --------------------------------------

def _set_passthrough_rcin3(vehicle, vtol_motor_channels):
    # Set channels to passthrough for RCIN3
    for channel in vtol_motor_channels:
        vehicle.parameters[f"SERVO{channel}_FUNCTION"] = 53

def _reset_original_params(vehicle, vtol_motor_channels, arming_check):    
    
    # Reset arming check value
    vehicle.parameters["ARMING_CHECK"] = arming_check  
    
    # Reset to VTOL motor functions
    for channel, servo_fn in zip(vtol_motor_channels, range(33,37)):
        vehicle.parameters[f"SERVO{channel}_FUNCTION"] = servo_fn

def ramp_motor(vehicle, pwm_start, pwm_stop, duration):

    start_time = time.time()
    ramp_steps = 8
    ramp_increment = int((pwm_stop - pwm_start)/ramp_steps)

    print(f"\nRamp: {pwm_start} us to {pwm_stop}")
    print(f"Ramp Increment: {ramp_increment} us\tRamp steps: {ramp_steps} steps")

    ramp_timer_start = time.time()
    for pwm in range(pwm_start, pwm_stop, ramp_increment):
        vehicle.channels.overrides[3] = pwm
        time.sleep(0.1)
    print(f"Ramp took {round((time.time() - ramp_timer_start), 3)} seconds")

    while (time.time()-start_time) <= duration:
        vehicle.channels.overrides[3] = pwm_stop
        time.sleep(0.25)

def spin_motor_sec(vehicle, pwm_out, duration=0):
    
    print(f"\nRunning motor at {pwm_out} us for {duration} seconds")
    
    # Send overrides at 4 Hz for duration greater than 0.25s
    if duration > 0.25:
        start_time = time.time()
        while (time.time()-start_time) <= duration:
            vehicle.channels.overrides[3] = pwm_out
            time.sleep(0.25)
    else:
        vehicle.channels.overrrides[3] = pwm_out
        time.sleep(duration)

def run_motor_profile(vehicle, pwm_esc, test_profile):
    
    # Unpack profile values
    spool_pct, spool_time = test_profile["spool"].values()
    peak_pct, peak_time = test_profile["peak"].values()
    hover_pct, hover_time = test_profile["hover"].values()

    # Unpack PWM values
    pwm_min, pwm_max = (pwm_esc.values())
    pwm_range = pwm_max - pwm_min

    # PWM values for each stage
    spool_pwm = int(pwm_min + (spool_pct * pwm_range))
    peak_pwm = int(pwm_min + (peak_pct * pwm_range))
    hover_pwm = int(pwm_min + (hover_pct * pwm_range))    

    # Arm vehicle
    vehicle.arm(wait=True)

    # Spool stage
    spin_motor_sec(vehicle, spool_pwm, spool_time)

    # Peak stage
    ramp_motor(vehicle, spool_pwm, peak_pwm, peak_time)

    # Hover stage
    spin_motor_sec(vehicle, hover_pwm, hover_time) 

    # Turn off motors
    print("\nTurning off VTOL motors")
    vehicle.channels.overrides = {'3': int(pwm_min)}
    vehicle.disarm(wait=True)



# --------------------------------------
# RUN SCRIPT
# --------------------------------------

# Connect to vehicle
vehicle = connect(CONNECTION_STRING, wait_ready=True)
print("\nConnected to vehicle")

# Backup params
_arming_check_backup = vehicle.parameters["ARMING_CHECK"]

try:
    # Setup CH 5-8 for passthrough from RCIN3
    _set_passthrough_rcin3(vehicle, VTOL_MOTOR_CHANNELS)
    
    test_start_time = time.time()
    # Arm vehicle, run motors & disarm
    run_motor_profile(vehicle, PWM_ESC, TEST_PROFILE)
    print(f"Time taken for motor profile test: {int(time.time() - test_start_time)} seconds")

    # Reset parameters
    _reset_original_params(vehicle, VTOL_MOTOR_CHANNELS, _arming_check_backup)

except KeyboardInterrupt:
        print("\nAborted by user, shutting motor...")
        vehicle.channels.overrides = {'3': PWM_ESC["min"]}
        vehicle.disarm(wait=True)
        _reset_original_params(vehicle, VTOL_MOTOR_CHANNELS, _arming_check_backup)
        sys.exit(0)


