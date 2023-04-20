import tkinter as tk
from tkinter import filedialog
import threading
import pandas as pd
import matplotlib.pyplot as plt
import serial
from datetime import datetime

# Define the global variables
continue_reading = False
csv = []

# Define the function to read from the serial port
def read_serial():
    global continue_reading, csv
    ser = serial.Serial('/dev/ttyUSB0', 19200)  # Change the serial port and baud rate as needed
    while continue_reading:
        line = ser.readline().decode().rstrip()
        if line:
            data = line.split(',')
            #if len(data) == 2:
            ozone_mixing_ratio = float(data[0])
            temperature = float(data[1])
            pressure = float(data[2])
            flow_rate = float(data[3])
            analog_input_1 = float(data[4])
            analog_input_2 = float(data[5])
            analog_input_3 = float(data[6])
            date = data[7]
            time_str = data[8]
            csv.append(data)
            update_label(f"Ozone: {ozone_mixing_ratio} ppbv, Temp: {temperature} K, Pressure: {pressure} torr")

# Define the function to start reading from the serial port
def start_reading():
    global continue_reading
    continue_reading = True
    # Start a new thread to run the read_serial() function
    threading.Thread(target=read_serial).start()

# Define the function to stop reading from the serial port
def stop_reading():
    global continue_reading,csv,filename
    continue_reading = False
    df = pd.DataFrame(csv, columns=['ozone_mixing_ratio','temperature','pressure',
                                'flow_rate','analog1','analog2','analog3','date',
                                'time'])
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f'{filename}.csv', index=False)
    update_label('Waiting for input...')

# Define the function to create a CSV file from the DataFrame
# def create_csv():
#     global csv, df, filename
#     df = pd.DataFrame(csv, columns=['ozone_mixing_ratio','temperature','pressure',
#                                 'flow_rate','analog1','analog2','analog3','date',
#                                 'time'])
#     filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     df.to_csv(f'{filename}.csv', index=False)

# Define the function to create a plot from the CSV
def create_plot():
    #df2 = pd.read_csv(f'/home/dusty/Desktop/2b_ozone/{filename}.csv')
    # Open a file dialog to select a CSV file
    filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if filename:
        # Load the CSV file into a DataFrame
        df2 = pd.read_csv(filename)
    df2.plot('time','ozone_mixing_ratio')
    #plt.savefig(f'/home/dusty/Desktop/2b_ozone/{filename}.png')
    plt.savefig(f'{filename}.png')

# Define a function to update the label with the latest data from the serial
def update_label(text):
    status_label.config(text=text)

# Define the GUI
root = tk.Tk()
root.geometry('400x200')
root.title('2BTech Ozone Logger')

# Define the GUI elements
start_button = tk.Button(root, text='Start', command=start_reading)
start_button.pack(pady=10)
stop_button = tk.Button(root, text='Stop', command=stop_reading)
stop_button.pack(pady=10)
# csv_button = tk.Button(root, text='Create CSV', command=create_csv)
# csv_button.pack(pady=10)
plot_button = tk.Button(root, text='Create Plot', command=create_plot)
plot_button.pack(pady=10)
status_label = tk.Label(root, text='Waiting for input...')
status_label.pack(pady=10)

root.mainloop()

