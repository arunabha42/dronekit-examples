import matplotlib.pyplot as plt
import pandas as pd
from pymavlink import mavutil

def plot_battery(logfile):
    # Open the log file
    mlog = mavutil.mavlink_connection(logfile)

    # Initialize empty lists to store data
    timestamps = []
    voltage = []
    current = []
    wattage = []

    # Iterate through all messages in the log
    while True:
        msg = mlog.recv_match(type='BAT', blocking=True)
        if msg is None:
            break

        # Extract data from the message
        timestamps.append(msg.TimeUS)
        voltage.append(msg.Volt)
        current.append(msg.Curr)
        wattage.append(msg.Volt * msg.Curr)

    # Create a DataFrame from the collected data
    df = pd.DataFrame({'Time': timestamps, 'Voltage': voltage, 'Current': current, 'Wattage': wattage})

    # Plot the data
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot voltage and current
    color = 'tab:blue'
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Voltage (V) / Current (A)', color=color)
    ax1.plot(df['Time'], df['Voltage'], label='Voltage (V)', color=color)
    ax1.plot(df['Time'], df['Current'], label='Current (A)', color='tab:red')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    # Create a secondary y-axis for wattage
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Wattage (W)', color=color)
    ax2.plot(df['Time'], df['Wattage'], label='Wattage (W)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper right')

    plt.title('Battery Voltage, Current, and Wattage vs Time')
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    logfile_path = "log_test_AS04_ATOL.bin"
    plot_battery(logfile_path)
