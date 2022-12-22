import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx import constants
import threading
from datetime import datetime
import time

# Parameters
sampling_freq_in = 12000  # in Hz
buffer_in_size = 48000
bufsize_callback = 1200
buffer_in_size_cfg = round(buffer_in_size) * 3  # clock configuration * 10 ?
chans_in = 3  # number of chan
refresh_rate_plot = 100000  # in Hz
crop = 0  # number of seconds to drop at acquisition start before saving

# Initialize data placeholders
buffer_in = np.zeros((chans_in, buffer_in_size))
data = np.zeros(
    (chans_in, 1))  # will contain a first column with zeros but that's fine
print(data.size)



# Definitions of basic functions
def ask_user():
    global running
    input("Press ENTER/RETURN to stop acquisition and coil drivers.")
    running = False


def cfg_read_task(acquisition):
    sensX=99.07e-6	#V/g
    sensY=97.08e-6	#V/g
    sensZ=101.7e-6	#V/g
    acquisition.ai_channels.add_ai_accel_chan("cDAQ9188Mod8/ai0",
			units=nidaqmx.constants.AccelUnits.METERS_PER_SECOND_SQUARED, 
			sensitivity=sensX, sensitivity_units=nidaqmx.constants.AccelSensitivityUnits.VOLTS_PER_G)	#Acc x
    acquisition.ai_channels.add_ai_accel_chan("cDAQ9188Mod8/ai1",
			units=nidaqmx.constants.AccelUnits.METERS_PER_SECOND_SQUARED, 
			sensitivity=sensY, sensitivity_units=nidaqmx.constants.AccelSensitivityUnits.VOLTS_PER_G)	#Acc y
    acquisition.ai_channels.add_ai_accel_chan("cDAQ9188Mod8/ai2",
			units=nidaqmx.constants.AccelUnits.METERS_PER_SECOND_SQUARED, 
			sensitivity=sensZ, sensitivity_units=nidaqmx.constants.AccelSensitivityUnits.VOLTS_PER_G)	#Acc y
    acquisition.timing.cfg_samp_clk_timing(rate=sampling_freq_in,
                                           sample_mode=constants.AcquisitionType.CONTINUOUS,
                                           samps_per_chan=buffer_in_size_cfg)


def reading_task_callback(task_idx, event_type, num_samples, callback_data):
    global data
    global buffer_in
    if running:
        t1 = time.time()
        buffer_in = np.zeros((chans_in, num_samples))  # double definition ???
        stream_in.read_many_sample(buffer_in, num_samples,
                                   timeout=constants.WAIT_INFINITELY)
        #buffer_in = np.zeros(3, dtype=np.float64)
        #stream_in.read_one_sample(buffer_in)
        # Convert the data from channel as a row order to channel as a column
        #data = buffer_in.T.astype(np.float32)
        # Do something with the data
        data = np.append(data, buffer_in,
                         axis=1)  # appends buffered data to total variable data
        print('Datos='+str(data)+' Tamano buffer='+str(num_samples))
        #f=np.fft.rfftfreq(data[4][1::].size,d=1/100000)
        #P=abs(np.fft.rfft(data[4][1::]))
        #plt.plot(f[f>200] ,P[f>200],'k')
        #plt.xlim(100,10000)
        #plt.plot(data[0][1::],'k--')
        t = time.time() - t1
        #self.datos["t_cdaq"] = t
        print(f't_cdaq={t*1000}ms')
        data = np.zeros((chans_in, 1))
    return 0


# Configure and setup the tasks
task_in = nidaqmx.Task()
cfg_read_task(task_in)
stream_in = AnalogMultiChannelReader(task_in.in_stream)
task_in.register_every_n_samples_acquired_into_buffer_event(bufsize_callback,
                                                            reading_task_callback)
# Start threading to prompt user to stop
thread_user = threading.Thread(target=ask_user)
thread_user.start()

# Main loop
running = True
time_start = datetime.now()
task_in.start()

# Plot a visual feedback for the user's mental health

# f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='all', sharey='none')
while running:  # make this adapt to number of channels automatically
    a = 0
    # ax1.clear()
    # ax2.clear()
    # ax3.clear()
    # ax1.plot(data[0, -sampling_freq_in * 5:].T,'r')  # 5 seconds rolling window
    # ax2.plot(data[1, -sampling_freq_in * 5:].T,'k')
    # ax3.plot(data[2, -sampling_freq_in * 5:].T,'b')
# Label and axis formatting
# ax3.set_xlabel('time [s]')
# ax1.set_ylabel('m/s**2')
# ax2.set_ylabel('m/s**2')
# ax3.set_ylabel('m/s**2')
# xticks = np.arange(0, data[0, -sampling_freq_in * 5:].size, sampling_freq_in)
# xticklabels = np.arange(0, xticks.size, 1)
# ax3.set_xticks(xticks)
# ax3.set_xticklabels(xticklabels)
# plt.pause(1/refresh_rate_plot)  # required for dynamic plot to work (if too low, nulling performance bad)
# Close task to clear connection once done
task_in.close()
duration = datetime.now() - time_start
print(duration, 'Pan t es mort')
experience_file = [duration, sampling_freq_in]
np.save('info.npy', experience_file)

# savefile:


# Some messages at the end
# print("\n")
# print("OPM acquisition ended.\n")
# print("Acquisition duration: {}.".format(duration))