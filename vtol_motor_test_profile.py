from multiprocessing.connection import wait
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
# FUNCTION DEFINITIONS
# --------------------------------------

def _set_passthrough_rcin3(vehicle, vtol_motor_channels):
    # Set channels to passthrough for RCIN3
    for channel in vtol_motor_channels:
        vehicle.parameters[f"SERVO{channel}_FUNCTION"] = 53

def _reset_original_params(vehicle, vtol_motor_channels, arming_check):    
    
    # Reset arming check value
    vehicle.parameters["ARMING_CHECK"] = arming_check    
    # Reset BRD_SAFETY_MASK
    vehicle.parameters["BRD_SAFETY_MASK"] = 0    
    # Reset to VTOL motor functions
    for channel, servo_fn in zip(vtol_motor_channels, range(33,37)):
        vehicle.parameters[f"SERVO{channel}_FUNCTION"] = servo_fn

def ramp_motor(vehicle, pwm_start, pwm_stop, duration):

    start_time = time.time()
    ramp_steps = 5
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

def spin_motor_sec(vehicle, pwm_min, pwm_max, duration, thr_out_pct=0.0):
    
    print(f"\nRunning motor at {int(thr_out_pct*100)}% for {duration} seconds")
    
    pwm_range = pwm_max - pwm_min
    pwm_out = int(pwm_min + pwm_range*thr_out_pct)
    
    # Overrides to be sent at 4 Hz in case ramp interval greater than 0.25s
    if duration > 0.25:
        start_time = time.time()
        while (time.time()-start_time) <= duration:
            vehicle.channels.overrides[3] = pwm_out
            time.sleep(0.25)
    else:
        vehicle.channels.overrrides[3] = pwm_out
        time.sleep(duration)

def run_motor_profile(vehicle, pwm_min, pwm_max, duration, hover_thr_pct):
    
    spool_sec = 4
    takeoff_sec = 2
    hover_sec = duration

    # q_m_spin_min = vehicle.parameters["Q_M_SPIN_MIN"]
    q_m_spin_min = 0.2
    pwm_spin_min = int(pwm_min + (q_m_spin_min * (pwm_max-pwm_min)))
    

    vehicle.arm(wait=True)

    # Spool at Q_M_SPIN_MIN for 2 seconds
    spin_motor_sec(vehicle, pwm_min, pwm_max, spool_sec, q_m_spin_min)

    # Takeoff - ramp to 80% over 2 seconds
    ramp_to = int(pwm_min + 0.4*(pwm_max-pwm_min))
    ramp_motor(vehicle, pwm_spin_min, ramp_to, takeoff_sec)

    # Hover at 75% for 40 seconds
    spin_motor_sec(vehicle, pwm_min, pwm_max, hover_sec, hover_thr_pct) 

    # Turn off motors
    print("\nTurning off VTOL motors")
    _pwm_out = int(pwm_min)
    vehicle.channels.overrides = {'3': _pwm_out}
    vehicle.disarm(wait=True)

# --------------------------------------
# USER PARAMS
# --------------------------------------
# CONNECTION_STRING = "com28"
# CONNECTION_STRING = "tcp:127.0.0.1:5763"
# CONNECTION_STRING = "udp:100.70.12.100:14690"

# CONNECTION_STRING = "tcp:100.93.85.117:5770"
CONNECTION_STRING = "tcp:127.0.0.1:5770"

RCIN_THROTTLE_CHANNEL = 3
VTOL_MOTOR_CHANNELS = range(5,9)
# TEST_DURATION_SECONDS = 40
# Test Parameters
HOVER_DURATION_SECONDS = 10
HOVER_THR_PCT = 0.35


# --------------------------------------
# RUN SCRIPT
# --------------------------------------

# Connect to vehicle
# vehicle = connect(CONNECTION_STRING, baud=57600, wait_ready=True)
vehicle = connect(CONNECTION_STRING, wait_ready=True)
print("\nConnected to vehicle")

# Backup params
_arming_check_backup = vehicle.parameters["ARMING_CHECK"]

# Allow VTOL motors output only
# VTOL motors are on channels 5-8
brd_safety_mask = int("0b00000011110000", 2)
vehicle.parameters["BRD_SAFETY_MASK"] = brd_safety_mask
print(f"\nSet param BRD_SAFETY_MASK = {brd_safety_mask}")

# Get ESC min & max values
# _q_m_pwm_max = int(vehicle.parameters["Q_M_PWM_MAX"])
# _q_m_pwm_min = int(vehicle.parameters["Q_M_PWM_MIN"])
_q_m_pwm_max = 2000
_q_m_pwm_min = 1000

print(f"Q_M_PWM_MIN = {_q_m_pwm_min} us")
print(f"Q_M_PWM_MAX = {_q_m_pwm_max} us")

try:
    # Setup CH 5-8 for passthrough from RCIN3
    _set_passthrough_rcin3(vehicle, VTOL_MOTOR_CHANNELS)
    
    test_start_time = time.time()
    # Arm vehicle, run motors & disarm
    run_motor_profile(vehicle, _q_m_pwm_min, _q_m_pwm_max, HOVER_DURATION_SECONDS, HOVER_THR_PCT)
    print(f"Time taken for motor profile test: {int(time.time() - test_start_time)} seconds")

    # Reset parameters
    _reset_original_params(vehicle, VTOL_MOTOR_CHANNELS, _arming_check_backup)

except KeyboardInterrupt:
        print("\nAborted by user, shutting motor...")
        vehicle.channels.overrides = {'3': _q_m_pwm_min}
        vehicle.disarm()
        _reset_original_params(vehicle, VTOL_MOTOR_CHANNELS, _arming_check_backup)
        sys.exit(0)


