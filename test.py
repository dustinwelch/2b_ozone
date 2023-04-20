import serial
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Change this to the serial port you are using
SERIAL_PORT = '/dev/ttyUSB0'
# Change this to match the baud rate of your serial communication
BAUD_RATE = 19200

# Open the serial port connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Create a list to store each line of data
csv = []
i=0
# Read and print data from the serial port indefinitely
while True:
    data = ser.readline().decode().rstrip()
    # Split the data string into separate values using the comma delimiter
    values = data.split(',')
    # Extract the values and convert to the appropriate data type
    ozone_mixing_ratio = float(values[0])
    temperature = float(values[1])
    pressure = float(values[2])
    flow_rate = float(values[3])
    analog_input_1 = float(values[4])
    analog_input_2 = float(values[5])
    analog_input_3 = float(values[6])
    date = values[7]
    time_str = values[8]
    csv.append(values)
    # Format the output string
    output_str = f"Ozone mixing ratio: {ozone_mixing_ratio:.2f} ppbv\n" \
                 f"Temperature: {temperature:.2f} K\n" \
                 f"Pressure: {pressure:.2f} torr\n" \
                 f"Flow rate: {flow_rate:.2f} cc/min\n" \
                 f"Analog input 1: {analog_input_1:.2f} V\n" \
                 f"Analog input 2: {analog_input_2:.2f} V\n" \
                 f"Analog input 3: {analog_input_3:.2f} V\n" \
                 f"Date: {date}\n" \
                 f"Time: {time_str}\n"

    # Print the output string to the console
    print(output_str)
    # Wait for the next data transmission
    time.sleep(10)
    i+=1
    if i >= 5:
        break

df = pd.DataFrame(csv, columns=['ozone_mixing_ratio','temperature','pressure',
                                'flow_rate','analog1','analog2','analog3','date',
                                'time'])
print(df)
date_now = datetime.now()
df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
filename = f'{date_now}_{time_str}'
df.to_csv(f'/home/dusty/Desktop/2b_ozone/{filename}.csv')
df2 = pd.read_csv(f'/home/dusty/Desktop/2b_ozone/{filename}.csv')
#plt.ylim(0, 15)
# plt.plot(df['time'],df['ozone_mixing_ratio'])
df2.plot('time','ozone_mixing_ratio')
plt.savefig(f'/home/dusty/Desktop/2b_ozone/{filename}.png')
plt.show()