import matplotlib.pyplot as plt
import pandas as pd
from pymavlink import mavutil

def plot_attitude(logfile):
    # Open the log file
    mlog = mavutil.mavlink_connection(logfile)

    # Initialize an empty list to store data
    data = []

    # Iterate through all messages in the log
    while True:
        msg = mlog.recv_match(type='ATT', blocking=True)
        if msg is None:
            break

        # Extract data from the message and append it to the list
        data.append({'Time': msg.TimeUS, 'DesRoll': msg.DesRoll, 'Roll': msg.Roll})

    # Print some debug information
    print("Number of messages:", len(data))

    # Create a DataFrame from the list
    df = pd.DataFrame(data)

    # Print the DataFrame for debugging
    print(df.head())

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time'], df['DesRoll'], label='DesRoll')
    plt.plot(df['Time'], df['Roll'], label='Roll')
    plt.xlabel('Time (ms)')
    plt.ylabel('Angle (degrees)')
    plt.title('ATT.DesRoll and ATT.Roll vs Time')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    logfile_path = "log_test_AS04_ATOL.bin"
    plot_attitude(logfile_path)
