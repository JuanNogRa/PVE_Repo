from PyQt5.QtCore import pyqtSignal,QThread
from daqhats import mcc152, OptionFlags, HatIDs, HatError, mcc128, AnalogInputMode, AnalogInputRange
from daqhats_utils import select_hat_device
import config

"""Hilo para generar voltaje usando el MCC 152."""
<<<<<<< HEAD
class SendVoltage():
    def main_sendVoltage(self, value):
=======
class SendVoltage(QThread):
    
    def __init__(self):
        QThread.__init__(self)
>>>>>>> 1647d561ef571c11ccc42be3ababb6c635157c87
        """
        This function is executed automatically when the module is run directly.
        """
        options = OptionFlags.DEFAULT
        channel = 0
        num_channels = mcc152.info().NUM_AO_CHANNELS

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
<<<<<<< HEAD
        message=value
        value = float(message)
        value = value/100.0
        #print('Voltage en hilo '+str(value))
        if (value < min_v) or (value > max_v):
            # Out of range, ask again.
            print("Value out of range.")
=======
        message=config.value
        print(message)
        if version_info.major > 2:
            str_v = input(message)
>>>>>>> 1647d561ef571c11ccc42be3ababb6c635157c87
        else:
            # Valid value.
            return value

"""Hilo para leer voltaje usando el MCC 128."""
class ReadVoltage(QThread):
    VoltageUpdate = pyqtSignal(list)
    def __init__(self):
        QThread.__init__(self)
        """
        This function is executed automatically when the module is run directly.
        """
        
        self.options = OptionFlags.DEFAULT
        self.low_chan = 0
        self.high_chan = 7
        input_mode = AnalogInputMode.SE
        input_range = AnalogInputRange.BIP_10V

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
                    samples_per_channel=0
<<<<<<< HEAD
                    self.VoltageUpdate.emit([sumCh0/samples_per_channel, sumCh1/samples_per_channel, sumCh2/samples_per_channel, sumCh3/samples_per_channel])
=======
                    self.VoltageUpdate.emit([sumCh0/100, sumCh1/100, sumCh2/100, sumCh3/100])
>>>>>>> 1647d561ef571c11ccc42be3ababb6c635157c87
                    sumCh0=0
                    sumCh1=0
                    sumCh2=0
                    sumCh3=0
            
    def stop(self):
        self.ThreadActive = False
        self.quit()

import time
import pigpio
import read_PWM

"""Hilo para leer frecuencia usando la libreria Pigpio."""
class ReadFrecuency(QThread):
    FrecuencyUpdate = pyqtSignal()
    """
    A class to read PWM pulses and calculate their frequency
    and duty cycle.  The frequency is how often the pulse
    happens per second.  The duty cycle is the percentage of
    pulse high time per cycle.
    """
    def __init__(self):
        QThread.__init__(self)
        
        PWM_GPIO = 4
        self.SAMPLE_TIME = 2.0

        pi = pigpio.pi()

        self.p = read_PWM.reader(pi, PWM_GPIO)

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            time.sleep(self.SAMPLE_TIME)
            f = self.p.frequency()
            self.FrecuencyUpdate.emit(f)

    def stop(self):
        self.ThreadActive = False
        self.quit()

    def _cbf(self, gpio, level, tick):

        if level == 1:

            if self._high_tick is not None:
                t = pigpio.tickDiff(self._high_tick, tick)

                if self._period is not None:
                    self._period = (self._old * self._period) + (self._new * t)
                else:
                    self._period = t

            self._high_tick = tick

        elif level == 0:

            if self._high_tick is not None:
                t = pigpio.tickDiff(self._high_tick, tick)

                if self._high is not None:
                    self._high = (self._old * self._high) + (self._new * t)
                else:
                    self._high = t

    def frequency(self):
        """
        Returns the PWM frequency.
        """
        if self._period is not None:
            return 1000000.0 / self._period
        else:
            return 0.0
