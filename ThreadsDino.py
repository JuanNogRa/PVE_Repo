from PyQt5.QtCore import pyqtSignal,QThread
from daqhats import mcc152, OptionFlags, HatIDs, HatError, mcc128, AnalogInputMode, AnalogInputRange
from daqhats_utils import select_hat_device
import config
import pigpio
import read_PWM
import time
import matplotlib
import socket
matplotlib.use('Qt5Agg')

"""Hilo para generar voltaje usando el MCC 152."""
class SendVoltage():
    def main_sendVoltage(self, value):
        """
        This function is executed automatically when the module is run directly.
        """
        options = OptionFlags.DEFAULT
        channel = 0
        num_channels = mcc152.info().NUM_AO_CHANNELS
        error = False
        # Ensure channel is valid.
        if channel not in range(num_channels):
            error_message = ('Error: Invalid channel selection - must be '
                            '0 - {}'.format(num_channels - 1))
            raise Exception(error_message)
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_152)
        hat = mcc152(address)
        
        #while self.ThreadActive and not error:
        value = self.get_input_value(value)
        # Write the value to the selected channel.
        try:
            hat.a_out_write(channel=channel,
                            value=value,
                            options=options)
        except (HatError, ValueError):
            error = True
        if error:
            print("Error al escribir en la salida analoga.")
                    
    def get_input_value(self, value):
        """Get the voltage from the user and validate it."""

        # Get the min and max voltage values for the analog outputs to validate
        # the user input.
        min_v = mcc152.info().AO_MIN_RANGE
        max_v = mcc152.info().AO_MAX_RANGE
        message=value
        value = float(message)
        #print('Voltage en hilo '+str(value))
        if (value < min_v) or (value > max_v):
            # Out of range, ask again.
            print("Value out of range.")
        else:
            # Valid value.
            return value
#import time
"""Hilo para leer voltaje usando el MCC 128."""
class ReadVoltage(QThread):
    VoltageUpdate = pyqtSignal(list)
    FrecuencyUpdate = pyqtSignal(list)
    def __init__(self, MinimaFrecuencia):
        QThread.__init__(self)
        """
        This function is executed automatically when the module is run directly.
        """
        
        self.options = OptionFlags.DEFAULT
        self.low_chan = 0
        self.high_chan = 7
        input_mode = AnalogInputMode.SE
        input_range = AnalogInputRange.BIP_2V

        mcc_128_num_channels = mcc128.info().NUM_AI_CHANNELS[input_mode]
        try:
            # Ensure low_chan and high_chan are valid.
            if self.low_chan < 0 or self.low_chan >= mcc_128_num_channels:
                error_message = ('Error: Invalid low_chan selection - must be '
                                '0 - {0:d}'.format(mcc_128_num_channels - 1))
                raise Exception(error_message)
            if self.high_chan < 0 or self.high_chan >= mcc_128_num_channels:
                error_message = ('Error: Invalid high_chan selection - must be '
                                '0 - {0:d}'.format(mcc_128_num_channels - 1))
                raise Exception(error_message)
            if self.low_chan > self.high_chan:
                error_message = ('Error: Invalid channels - high_chan must be '
                                'greater than or equal to low_chan')
                raise Exception(error_message)
        except (HatError, ValueError) as error:
            print('\n', error)
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_128)
        self.hat = mcc128(address)
        self.hat.a_in_mode_write(input_mode)
        self.hat.a_in_range_write(input_range)
        QThread.__init__(self)
        
        PWM_GPIO = 17
        #self.SAMPLE_TIME = 2.0

        self.pi = pigpio.pi()
        self.p = read_PWM.reader(self.pi, PWM_GPIO, MinimaFrecuencia)
        self.counter_cycles=0
        
    def run(self):
        samples_per_channel = 0
        sumCh0=0
        sumCh1=0
        sumCh2=0
        sumCh3=0
        canales_lectura = [0, 1, 4, 5]                      # Canales a usar para leer voltaje.
        self.ThreadActive = True
        error = False
        while self.ThreadActive and not error:
                #start=time.time()
            # Display the updated samples per channel count
                samples_per_channel += 1
                #print('\r{:17}'.format(samples_per_channel), end='')

                # Read a single value from each selected channel.
                for chan in canales_lectura:
                    value = self.hat.a_in_read(chan, self.options)
                    if (chan==0):
                        sumCh0=sumCh0+value
                    if (chan==1):
                        sumCh1=sumCh1+value
                    if (chan==4):
                        sumCh2=sumCh2+value
                    if (chan==5):
                        sumCh3=sumCh3+value
                    #print('{:12.5} V'.format(value), end='')
                if (samples_per_channel==100):
                    self.VoltageUpdate.emit([sumCh0/samples_per_channel, sumCh1/samples_per_channel, sumCh2/samples_per_channel, sumCh3/samples_per_channel])
                    samples_per_channel=0
                    sumCh0=0
                    sumCh1=0
                    sumCh2=0
                    sumCh3=0
                f = self.p.frequency()
                    #self.p._counter_pulses = 0
                if (config.startTest_activacte==True):
                    self.counter_cycles = self.p._counter_pulses
                else:
                    self.p._counter_pulses = 0
                    #self.counter_cycles = self.p._counter_pulses
                
                if f is not None:
                    self.FrecuencyUpdate.emit([f, self.counter_cycles])
                else:
                    self.FrecuencyUpdate.emit([0, self.counter_cycles]) 
                                   
    
                #end = time.time()
                #print('Tiempo '+str(end - start))
    def stop(self):
        self.ThreadActive = False
        self.p.cancel()
        self.pi.stop()
        self.quit()
        
class Do_every(QThread):
    Muestreo_Time = pyqtSignal(float)
    def __init__(self, period):
        QThread.__init__(self)
        self.period = period
        
    def run(self):
        self.ThreadActive=True
        g = self.g_tick()
        while self.ThreadActive:
            self.start=time.time()
            time.sleep(next(g))
            self.Muestreo_Time.emit(time.time()-self.start)
            config.f=True
    
    def g_tick(self):
        t = time.time()
        while self.ThreadActive:
            t += self.period
            yield max(t - time.time(),0)
                
    def stop(self):
        self.ThreadActive = False
        self.quit()

class SocketComunication(QThread):
    Client_address = pyqtSignal(tuple)
    
    def __init__(self, HOST):
        QThread.__init__(self)
        self.HOST=HOST
        
    def run(self):
        self.ThreadActive=True
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address given on the command line
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 1338))
            s.listen()
            conn, addr = s.accept()
            with conn:
                self.Client_address.emit(addr)
                while self.ThreadActive:
                    
                    #index = int(self.muestreo*self.muestreo_time)
                        #self.data_line3.setData(self.cycledrive_data[:,0],  self.cycledrive_data[:,1])  # Update the data.
                    data = conn.recv(1024)
                    if not data:
                        break
                    data = str(config.Velocidad).encode('utf8')
                    #print(data)
                    conn.send(data)

                    data = conn.recv(1024)
                    if not data:
                        break
                    data = str(config.Velocidad_perfil).encode('utf8')
                    #print(data)
                    conn.send(data)
   

    def stop(self):
        self.ThreadActive = False
        self.quit()