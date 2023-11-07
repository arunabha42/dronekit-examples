serdev = 'COM43' # serial device of JeVois
  
import serial
import time
import jevoisData
  
def read_serial_data():
    with serial.Serial(serdev, 115200) as ser:
        while 1:
        # Read a whole line and strip any trailing line ending character:
            time.sleep(0.15)
            line = ser.readline().decode("utf-8").rstrip()
            #print ("received: {}".format(line))
            return line

def offsetData():
    while True:
        # Generate a random message
        message = jevoisData.fakeData()
        print("Generated Message:", message)

        # Split the message by spaces to extract values
        values = message.split()
        
        if len(values) >= 7:
            x = int(values[2])
            y = int(values[3])
            XYOffset = [x, y]
            return XYOffset
        else:
            print("Invalid message format.")

        # Sleep for a while before generating the next message
        time.sleep(0.33)


