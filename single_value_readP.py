#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 128 Functions Demonstrated:
        mcc128.a_in_read
        mcc128.a_in_mode_write
        mcc128.a_in_range_write

    Purpose:
        Read a single data value for each channel in a loop.

    Description:
        This example demonstrates acquiring data using a software timed loop
        to read a single value from each selected channel on each iteration
        of the loop.
"""
from __future__ import print_function
import time
from time import sleep
from sys import stdout
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'
sensibilidadCeldas, capacidadCeldas, factorAmplificacion = 0.003, 2000, 100

def main():
    """
    This function is executed automatically when the module is run directly.
    """
    options = OptionFlags.DEFAULT
    low_chan = 0
    high_chan = 4
    input_mode = AnalogInputMode.SE
    input_range = AnalogInputRange.BIP_2V

    mcc_128_num_channels = mcc128.info().NUM_AI_CHANNELS[input_mode]
    sample_interval = 0.5  # Seconds

    try:
        # Ensure low_chan and high_chan are valid.
        if low_chan < 0 or low_chan >= mcc_128_num_channels:
            error_message = ('Error: Invalid low_chan selection - must be '
                             '0 - {0:d}'.format(mcc_128_num_channels - 1))
            raise Exception(error_message)
        if high_chan < 0 or high_chan >= mcc_128_num_channels:
            error_message = ('Error: Invalid high_chan selection - must be '
                             '0 - {0:d}'.format(mcc_128_num_channels - 1))
            raise Exception(error_message)
        if low_chan > high_chan:
            error_message = ('Error: Invalid channels - high_chan must be '
                             'greater than or equal to low_chan')
            raise Exception(error_message)

        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_128)
        hat = mcc128(address)

        hat.a_in_mode_write(input_mode)
        hat.a_in_range_write(input_range)

        print('\nMCC 128 single data value read example')
        print('    Functions demonstrated:')
        print('         mcc128.a_in_read')
        print('         mcc128.a_in_mode_write')
        print('         mcc128.a_in_range_write')
        print('    Input mode: ', input_mode_to_string(input_mode))
        print('    Input range: ', input_range_to_string(input_range))
        print('    Channels: {0:d} - {1:d}'.format(low_chan, high_chan))
        print('    Options:', enum_mask_to_string(OptionFlags, options))
        try:
            input("\nPress 'Enter' to continue")
        except (NameError, SyntaxError):
            pass

        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\n  Samples/Channel', end='')
        for chan in range(low_chan, high_chan + 1):
            print('     Channel', chan, end='')
        print('')

        try:
           
            while True:
                samples_per_channel = 0
                sumCh0, sumCh4 = 0, 0
                inicio=time.time()
                while time.time()-inicio<1:
                    # Display the updated samples per channel count
                    samples_per_channel += 1

                    # Read a single value from each selected channel.
                    for chan in range(0, 5, 4):
                        value = hat.a_in_read(chan, options)
                        if chan == 0:
                            sumCh0 += value
                        if chan == 4:
                            sumCh4 += value
                print('Voltaje Canal 0: {:.5f}'.format(sumCh0/samples_per_channel, ' V   '),
                      'Voltaje Canal 4: {:.5f}'.format(sumCh4/samples_per_channel, ' V   '))
                print('Muestras '+str(samples_per_channel))
		#print('Peso 0: {:.2f}'.format(capacidadCeldas*(sumCh0/100)/
                     #(factorAmplificacion*sensibilidadCeldas*5)))
                # Wait the specified interval between reads.

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
