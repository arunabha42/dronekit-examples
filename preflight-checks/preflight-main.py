import time
from dronekit import connect
import preflightHelpers

connection_string = "tcp:127.0.0.1:5762"

vehicle = connect(connection_string)

# -------- PREFLIGHT CHECK ---------

# AIRSPEED CHECK
preflightHelpers.check_airspeed()

# RANGEFINDER CHECK


# BATTERY CHECKS

# GPS CHECKS

# EKF CHECKS

# ATTITUDE CHECKS