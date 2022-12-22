#!/usr/bin/env python

# read_PWM.py
# 2015-12-08
# Public Domain

import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import time
class reader:
   """
   A class to read PWM pulses and calculate their frequency
   and duty cycle.  The frequency is how often the pulse
   happens per second.  The duty cycle is the percentage of
   pulse high time per cycle.
   """
   def __init__(self, pi, gpio, MinimaFrecuencia, weighting=0.0):
      """
      Instantiate with the Pi and gpio of the PWM signal
      to monitor.

      Optionally a weighting may be specified.  This is a number
      between 0 and 1 and indicates how much the old reading
      affects the new reading.  It defaults to 0 which means
      the old reading has no effect.  This may be used to
      smooth the data.
      """
      self.pi = pi
      self.gpio = gpio
      self.MinimaFrecuencia = MinimaFrecuencia
      
      if weighting < 0.0:
         weighting = 0.0
      elif weighting > 0.99:
         weighting = 0.99

      self._new = 1.0 - weighting # Weighting for new reading.
      self._old = weighting       # Weighting for old reading.

      self._high_tick = None
      self._low_tick = None
      self._period = None
      self._high = None
      self._counter_pulses = 0
      self._startTime = time.time()
      self._timeTotal = 0
      pi.set_mode(gpio, pigpio.INPUT)

      self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

   def _cbf(self, gpio, level, tick):
      if level == 1:
         
         self._counter_pulses += 1
         
         if self._high_tick is not None:
            t = pigpio.tickDiff(self._high_tick, tick)
            self._startTime=time.time()
            if self._period is not None:
               self._period = (self._old * self._period) + (self._new * t)
            else:
               self._period = t
         self._high_tick = tick

   def frequency(self):
      """
      Returns the PWM frequency.
      """
      self._timeTotal = time.time()-self._startTime
      #print(self._timeTotal)
      if self._period is not None:
          if ((self._timeTotal) > 1/(self.MinimaFrecuencia) or 1000000.0 / self._period < (self.MinimaFrecuencia)):
             #self._period=None
             return None
          else:
             return 1000000.0 / self._period
      else:
         return None
      
      

   def cancel(self):
      """
      Cancels the reader and releases resources.
      """
      self._cb.cancel()
