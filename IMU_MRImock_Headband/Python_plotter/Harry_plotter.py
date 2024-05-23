import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the serial line
ser = serial.Serial('COM5', 115200)  # Change 'COM3' to your specific serial port

# Parameters for plotting
max_len = 300  # Number of points to display on the graph

# Initialize empty lists for data
ax_data = []
ay_data = []
az_data = []
gx_data = []
gy_data = []
gz_data = []

# Create figure for plotting
fig, (ax, gx) = plt.subplots(2, 1)
ax.set_title('Accelerometer Data')
gx.set_title('Gyroscope Data')

# Initialize plots
ax_ax_line, = ax.plot([], [], label='AX')
ax_ay_line, = ax.plot([], [], label='AY')
ax_az_line, = ax.plot([], [], label='AZ')
gx_gx_line, = gx.plot([], [], label='GX')
gx_gy_line, = gx.plot([], [], label='GY')
gx_gz_line, = gx.plot([], [], label='GZ')

ax.set_xlabel('Time')
ax.set_ylabel('Acceleration (mg)')
ax.grid(True)
gx.set_xlabel('Time')
gx.set_ylabel('mdps')
gx.grid(True)

ax.legend()
gx.legend()

# Function to update the plot
def update_plot(frame):
    line = ser.readline().decode('utf-8').strip()
    if line.startswith("AX:"):
        parts = line.split(" ")
        ax_data.append(float(parts[0].split(":")[1]))
        ay_data.append(float(parts[1].split(":")[1]))
        az_data.append(float(parts[2].split(":")[1]))
        gx_data.append(float(parts[3].split(":")[1]))
        gy_data.append(float(parts[4].split(":")[1]))
        gz_data.append(float(parts[5].split(":")[1]))

        if len(ax_data) > max_len:
            ax_data.pop(0)
            ay_data.pop(0)
            az_data.pop(0)
            gx_data.pop(0)
            gy_data.pop(0)
            gz_data.pop(0)

        ax_ax_line.set_data(range(len(ax_data)), ax_data)
        ax_ay_line.set_data(range(len(ay_data)), ay_data)
        ax_az_line.set_data(range(len(az_data)), az_data)
        gx_gx_line.set_data(range(len(gx_data)), gx_data)
        gx_gy_line.set_data(range(len(gy_data)), gy_data)
        gx_gz_line.set_data(range(len(gz_data)), gz_data)

        ax.relim()
        ax.autoscale_view()
        gx.relim()
        gx.autoscale_view()

    return ax_ax_line, ax_ay_line, ax_az_line, gx_gx_line, gx_gy_line, gx_gz_line

# Set up plot to call update function periodically
ani = animation.FuncAnimation(fig, update_plot, interval=50, cache_frame_data=False)

plt.show()
