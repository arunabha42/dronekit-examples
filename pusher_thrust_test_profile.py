import sys
import time
import argparse

from dronekit import connect
from pymavlink import mavutil

'''
1. Connect to vehicle
2. Ramp motor to 100%
3. Reset throttle to zero
'''

# --------------------------------------
# ARGS
# --------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--half', type=int, required=True, help="1: 0-50%\t2:50-100%")

args = parser.parse_args()

# --------------------------------------
# USER PARAMS
# --------------------------------------
CONNECTION_STRING = "tcp:127.0.0.1:5763"
# CONNECTION_STRING = "udp:100.70.12.100:14690"
NUM_READINGS = 10
THROTTLE_STEP_DURATION = 1
RCIN_THROTTLE_CHANNEL = 3
RCOUT_MOTOR_CHANNEL = 3


# --------------------------------------
# FUNCTION DEFINITIONS
# --------------------------------------

def _reset_originals():
    # Reset throttle to zero
    vehicle.channels.overrides[3] = test_thr_out_min
    # Disarm throttle
    vehicle.disarm()
    # Reset arming check value
    vehicle.parameters["ARMING_CHECK"] = _arming_check_backup
    # Reset BRD_SAFETY_MASK
    vehicle.parameters["BRD_SAFETY_MASK"] = 0

def run_motor(vehicle, test_thr_out_min, test_thr_out_max, pwm_interval):
    
    global args
    for pwm_us in range(test_thr_out_min, (test_thr_out_max+1), pwm_interval):

        
        global param_throttle_out_min, param_throttle_out_max
        _thr_pct = round((pwm_us - param_throttle_out_min) / (param_throttle_out_max - param_throttle_out_min) * 100)
        print(f"\nThrottle:\t{_thr_pct} %", file=f)
        print(f"PWM:\t\t{pwm_us} us", file=f)

        # Current accumulator
        _current_acc = []

        try:
            start_time = time.time()
            # Run throttle for duration
            while time.time()-start_time < THROTTLE_STEP_DURATION:
                vehicle.channels.overrides[3] = pwm_us
                _current_acc.append(vehicle.battery.current)
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nAborted by user, shutting motor...", file=f)
            vehicle.channels.overrides[3] = test_thr_out_min
            _reset_originals()
            sys.exit(0)

        _current_avg = round(sum(_current_acc) / len(_current_acc), 1)
        print(f"Current avg:\t{_current_avg} A", file=f)




# Connect to vehicle
vehicle = connect(CONNECTION_STRING, wait_ready=True)
print("\nConnected to vehicle")

# Backup params
_arming_check_backup = vehicle.parameters["ARMING_CHECK"]

# Allow throttle output only
brd_safety_mask = int("0b00100000000000", 2)
vehicle.parameters["BRD_SAFETY_MASK"] = brd_safety_mask
print(f"\nSet param BRD_SAFETY_MASK = {brd_safety_mask}")

#  Get MIN & MAX PWM for throttle output
param_throttle_out_max = int(vehicle.parameters[f"SERVO{RCOUT_MOTOR_CHANNEL}_MAX"])
param_throttle_out_min = int(vehicle.parameters[f"SERVO{RCOUT_MOTOR_CHANNEL}_MIN"])

print(f"\nVehicle params for motor output")
print(f"SERVO{RCOUT_MOTOR_CHANNEL}_MAX: {param_throttle_out_max}")
print(f"SERVO{RCOUT_MOTOR_CHANNEL}_MIN: {param_throttle_out_min}")

# Set PWM range to be used for motor test
mid_throttle = int((param_throttle_out_min+param_throttle_out_max)/2)
test_thr_out_min = param_throttle_out_min if (args.half == 1) else mid_throttle
test_thr_out_max = mid_throttle if (args.half == 1) else param_throttle_out_max

print("\nThrottle range for test:")
print(f"Min PWM: {test_thr_out_min}")
print(f"Max PWM: {test_thr_out_max}")

# Test points & Interval
pwm_interval = int((test_thr_out_max - test_thr_out_min)/NUM_READINGS)
print(f"\nNo of readings: {NUM_READINGS}\nPWM Interval: {pwm_interval} us")

# --------------------------------------
# Run throttle test profile
# --------------------------------------

# Arm throttle
print("Arming throttle now...")
vehicle.parameters["ARMING_CHECK"] = 0
vehicle.arm(wait=True)
print("\nThrottle ARMED, proceeding to test motor in 2 seconds...")
time.sleep(2)

# Run motor
log_txt = run_motor(vehicle, test_thr_out_min, test_thr_out_max, pwm_interval)

# Disarm, reset overrides & parameters 
_reset_originals()