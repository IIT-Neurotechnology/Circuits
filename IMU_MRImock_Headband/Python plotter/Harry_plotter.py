import serial
import time
import matplotlib.pyplot as plt

# Serial port configuration
ser = serial.Serial('COM3', 115200)  # Adjust 'COM3' to your serial port
time.sleep(2)  # Wait for the serial connection to initialize

# Data storage
time_data = []

# Acceleration data
ax_data = []
ay_data = []
az_data = []

# Gyroscope data
gx_data = []
gy_data = []
gz_data = []

# Plot configuration for acceleration
plt.ion()
fig1, ax1 = plt.subplots()
line1, = ax1.plot(time_data, ax_data, 'r-', label='AX')
line2, = ax1.plot(time_data, ay_data, 'g-', label='AY')
line3, = ax1.plot(time_data, az_data, 'b-', label='AZ')

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Acceleration (m/s^2)')
ax1.set_title('Acceleration Data')
ax1.legend()

# Plot configuration for gyroscope
fig2, ax2 = plt.subplots()
line4, = ax2.plot(time_data, gx_data, 'r-', label='GX')
line5, = ax2.plot(time_data, gy_data, 'g-', label='GY')
line6, = ax2.plot(time_data, gz_data, 'b-', label='GZ')

ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Gyroscope (dps)')
ax2.set_title('Gyroscope Data')
ax2.legend()

start_time = time.time()

while True:
    line = ser.readline().decode('utf-8').strip()
    
    if line.startswith("AX:"):
        # Parsing acceleration data
        parts = line.split(',')
        ax = float(parts[0].split(':')[1])
        ay = float(parts[1].split(':')[1])
        az = float(parts[2].split(':')[1])

        current_time = time.time() - start_time
        time_data.append(current_time)
        ax_data.append(ax)
        ay_data.append(ay)
        az_data.append(az)

        # Update acceleration plot
        line1.set_xdata(time_data)
        line1.set_ydata(ax_data)
        line2.set_xdata(time_data)
        line2.set_ydata(ay_data)
        line3.set_xdata(time_data)
        line3.set_ydata(az_data)

        ax1.relim()
        ax1.autoscale_view()
        fig1.canvas.draw()
        fig1.canvas.flush_events()

    elif line.startswith("GX:"):
        # Parsing gyroscope data
        parts = line.split(',')
        gx = float(parts[0].split(':')[1])
        gy = float(parts[1].split(':')[1])
        gz = float(parts[2].split(':')[1])

        current_time = time.time() - start_time
        gx_data.append(gx)
        gy_data.append(gy)
        gz_data.append(gz)

        # Update gyroscope plot
        line4.set_xdata(time_data)
        line4.set_ydata(gx_data)
        line5.set_xdata(time_data)
        line5.set_ydata(gy_data)
        line6.set_xdata(time_data)
        line6.set_ydata(gz_data)

        ax2.relim()
        ax2.autoscale_view()
        fig2.canvas.draw()
        fig2.canvas.flush_events()
