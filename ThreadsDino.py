from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSignal,QThread, Qt, QMutex 
from daqhats import mcc152, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device
from sys import version_info
from __future__ import print_function
import config

class SendVoltage(QThread):
    
    def __init__(self, path, activateRectification):
        QThread.__init__(self)
        """
        This function is executed automatically when the module is run directly.
        """
        self.options = OptionFlags.DEFAULT
        self.channel = 0
        num_channels = mcc152.info().NUM_AO_CHANNELS

        # Ensure channel is valid.
        if self.channel not in range(num_channels):
            error_message = ('Error: Invalid channel selection - must be '
                            '0 - {}'.format(num_channels - 1))
            raise Exception(error_message)
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_152)
        self.hat = mcc152(address)
        
        
    def run(self):
        self.ThreadActive = True
        error = False
        while self.ThreadActive and not error:
            try:
                value = self.get_input_value()
            except ValueError:
                run_loop = False
            else:
                # Write the value to the selected channel.
                try:
                    self.hat.a_out_write(channel=self.channel,
                                value=value,
                                options=self.options)
                except (HatError, ValueError):
                    error = True
        if error:
            print("Error al escribir en la salida analoga.")
    def stop(self):
        self.ThreadActive = False
        self.quit()

    def get_input_value(self):
        """Get the voltage from the user and validate it."""

        # Get the min and max voltage values for the analog outputs to validate
        # the user input.
        min_v = mcc152.info().AO_MIN_RANGE
        max_v = mcc152.info().AO_MAX_RANGE
        message=config.value
        if version_info.major > 2:
            str_v = input(message)
        else:
            str_v = raw_input(message)

        try:
            value = float(str_v)
            value = value/100.0
        except ValueError:
            raise
        else:
            if (value < min_v) or (value > max_v):
                # Out of range, ask again.
                print("Value out of range.")
            else:
                # Valid value.
                return value