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
    global continue_reading, csv, last_reading
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
            #update_label(f"Ozone: {ozone_mixing_ratio} ppbv, Temp: {temperature} K, Pressure: {pressure} torr")
            last_reading = {'ozone_mixing_ratio': ozone_mixing_ratio, 'temperature': temperature,
                            'pressure': pressure}

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
    global df2, filename
    #df2 = pd.read_csv(f'/home/dusty/Desktop/2b_ozone/{filename}.csv')
    # Open a file dialog to select a CSV file
    filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if filename:
        # Load the CSV file into a DataFrame
        df2 = pd.read_csv(filename)
        # Create a new popup window to select the time range
        popup = tk.Toplevel()
        popup.geometry('300x150')
        popup.title('Select Time Range')
        start_label = tk.Label(popup, text='Start Time (HH:MM:SS)')
        start_label.pack(pady=5)
        start_entry = tk.Entry(popup)
        start_entry.pack(pady=5)
        end_label = tk.Label(popup, text='End Time (HH:MM:SS)')
        end_label.pack(pady=5)
        end_entry = tk.Entry(popup)
        end_entry.pack(pady=5)
        ok_button = tk.Button(popup, text='OK', command=lambda: plot_selected_range(df2, start_entry.get(), end_entry.get()))
        ok_button.pack(pady=10)
    #df2.plot('time','ozone_mixing_ratio')
    #plt.savefig(f'/home/dusty/Desktop/2b_ozone/{filename}.png')
    #plt.savefig(f'{filename}.png')

# Define the function to plot the selected time range
def plot_selected_range(df, start_time, end_time):
    # Convert the start and end times to datetime objects
    start_datetime = pd.to_datetime(start_time).time()
    end_datetime = pd.to_datetime(end_time).time()
    # Filter the DataFrame based on the selected time range
    mask = (df2['time'].apply(lambda x: pd.to_datetime(x).time()) >= start_datetime) & (df2['time'].apply(lambda x: pd.to_datetime(x).time()) <= end_datetime)
    df = df.loc[mask]
    # Create the plot from the filtered DataFrame
    df2.plot('time','ozone_mixing_ratio')
    # Display the plot
    plt.savefig(f'{filename}.png')

# Define a function to update the label with the latest data from the serial
# def update_label(text):
#     status_label.config(text=text)

def update_label():
    global status_text
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{now}: {last_reading}\n"
    status_text.insert(tk.END, line)
    status_text.see(tk.END)
    # Keep only the last 10 lines
    _, *lines = status_text.get("1.0", tk.END).split("\n")
    if len(lines) > 10:
        status_text.delete("1.0", f"{tk.END} - {len(lines[0])} chars")

# Define the GUI
# root = tk.Tk()
# root.geometry('400x200')
# root.title('2BTech Ozone Logger')

# # Define the GUI elements
# start_button = tk.Button(root, text='Start', command=start_reading)
# start_button.pack(pady=10)
# stop_button = tk.Button(root, text='Stop', command=stop_reading)
# stop_button.pack(pady=10)
# # csv_button = tk.Button(root, text='Create CSV', command=create_csv)
# # csv_button.pack(pady=10)
# plot_button = tk.Button(root, text='Create Plot', command=create_plot)
# plot_button.pack(pady=10)
# status_label = tk.Label(root, text='Waiting for input...')
# status_label.pack(pady=10)

def create_gui():
    global start_button, stop_button, csv_button, status_text, status_scrollbar
    root = tk.Tk()
    root.geometry('400x300')
    root.title('Serial Port Reader')

    # Define the GUI elements
    start_button = tk.Button(root, text='Start', command=start_reading)
    start_button.pack(pady=10)
    stop_button = tk.Button(root, text='Stop', command=stop_reading)
    stop_button.pack(pady=10)
    # csv_button = tk.Button(root, text='Create CSV', command=create_csv)
    # csv_button.pack(pady=10)

    # Create a scrollable status label
    status_frame = tk.Frame(root)
    status_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    status_label = tk.Label(status_frame, text='Status:')
    status_label.pack(side=tk.TOP, fill=tk.X)
    status_text = tk.Text(status_frame, wrap=tk.WORD, height=10)
    status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    status_scrollbar = tk.Scrollbar(status_frame)
    status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    status_text.config(yscrollcommand=status_scrollbar.set)
    status_scrollbar.config(command=status_text.yview)

    root.mainloop()

if __name__ == '__main__':
    create_gui()