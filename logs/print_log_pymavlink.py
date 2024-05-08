from pymavlink import mavutil

def print_messages(logfile, message_types):
    # Open the log file
    mlog = mavutil.mavlink_connection(logfile)

    # Iterate through all messages in the log
    while True:
        msg = mlog.recv_msg()
        if msg is None:
            break

        # Check if the message type is one of the specified types
        if msg.get_type() in message_types:
            print(msg)
            break

# Example usage
if __name__ == "__main__":
    logfile_path = "log_test_AS04_ATOL.bin"
    # Specify the message types you're interested in
    message_types = ["BAT"]  # Add more message types as needed
    print_messages(logfile_path, message_types)
