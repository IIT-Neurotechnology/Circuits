import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from collections import deque
import threading
import serial.tools.list_ports
import csv
import tkinter as tk
from tkinter import filedialog

# Function to open a file dialog for saving the file
def ask_for_file_path():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path

file_path = ask_for_file_path()

if not file_path:
    raise Exception("No file selected. Exiting program.")

ports = list(serial.tools.list_ports.comports())
for p in ports:
    if "3315221F37323835B61A33324B572D45" in p.serial_number:
        print("IMU found!")
        ser = serial.Serial(p.device, 115200)

# Parameters for plotting
max_len = 300  # Number of points to display on the graph

# Initialize deques for data
timestamps = deque(maxlen=max_len)
ax_data = deque(maxlen=max_len)
ay_data = deque(maxlen=max_len)
az_data = deque(maxlen=max_len)
gx_data = deque(maxlen=max_len)
gy_data = deque(maxlen=max_len)
gz_data = deque(maxlen=max_len)

# Create figure for plotting
fig, (ax, gx) = plt.subplots(2, 1)
ax.set_title('Accelerometer Data')
gx.set_title('Gyroscope Data')
tstart = time.time()

# Initialize plots
ax_ax_line, = ax.plot([], [], label='AX')
ax_ay_line, = ax.plot([], [], label='AY')
ax_az_line, = ax.plot([], [], label='AZ')
gx_gx_line, = gx.plot([], [], label='GX')
gx_gy_line, = gx.plot([], [], label='GY')
gx_gz_line, = gx.plot([], [], label='GZ')

ax.set_xlabel('Time (s)')
ax.set_ylabel('mg')
ax.grid(True)
gx.set_xlabel('Time (s)')
gx.set_ylabel('mdps')
gx.grid(True)

ax.legend()
gx.legend()

# Thread-safe queue for serial data
data_queue = deque(maxlen=1)

# Open the CSV file for writing data
with open(file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header
    csvwriter.writerow(['Time', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ'])

    def read_serial_data():
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("AX:"):
                data_queue.append(line)
                # Write data to the CSV file
                parts = line.split(" ")
                current_time = time.time() - tstart
                ax_value = float(parts[0].split(":")[1])
                ay_value = float(parts[1].split(":")[1])
                az_value = float(parts[2].split(":")[1])
                gx_value = float(parts[3].split(":")[1])
                gy_value = float(parts[4].split(":")[1])
                gz_value = float(parts[5].split(":")[1])
                csvwriter.writerow([current_time, ax_value, ay_value, az_value, gx_value, gy_value, gz_value])

    # Start the serial reading thread
    serial_thread = threading.Thread(target=read_serial_data)
    serial_thread.daemon = True
    serial_thread.start()

    # Function to update the plot
    def update_plot(frame):
        if data_queue:
            line = data_queue.popleft()
            parts = line.split(" ")
            current_time = time.time() - tstart
            timestamps.append(current_time)
            ax_data.append(float(parts[0].split(":")[1]))
            ay_data.append(float(parts[1].split(":")[1]))
            az_data.append(float(parts[2].split(":")[1]))
            gx_data.append(float(parts[3].split(":")[1]))
            gy_data.append(float(parts[4].split(":")[1]))
            gz_data.append(float(parts[5].split(":")[1]))

            ax_ax_line.set_data(timestamps, ax_data)
            ax_ay_line.set_data(timestamps, ay_data)
            ax_az_line.set_data(timestamps, az_data)
            gx_gx_line.set_data(timestamps, gx_data)
            gx_gy_line.set_data(timestamps, gy_data)
            gx_gz_line.set_data(timestamps, gz_data)

            ax.relim()
            ax.autoscale_view()
            gx.relim()
            gx.autoscale_view()

        return ax_ax_line, ax_ay_line, ax_az_line, gx_gx_line, gx_gy_line, gx_gz_line

    # Set up plot to call update function periodically
    ani = animation.FuncAnimation(fig, update_plot, interval=5, blit=True, cache_frame_data=False)

    plt.show()
