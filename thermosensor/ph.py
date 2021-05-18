import time,sys,math
from grove.adc import ADC

__all__ = ["GrovePhSensor"]

class GrovePhSensor(object):

        def __init__(self, channel):
                self.channel = channel
                self.adc = ADC()
        @property
        def value(self):
                return self.adc.read(self.channel)

def main():
#Connect the Grove PH Sensor to analog port A0
        # SIG,NC,VCC,GND
        sensor = GrovePhSensor(0)


        # Reference voltage of ADC is 4.95v
        Vref = 4.95

        while True:
                try:
                # Read sensor value
                # sensor_value = grove.analogRead(sensor)
                # Calculate PH
                # 7 means the neutral PH value,372 means the Reference value of ADC measured under neutral pH
                # 59.16=Conversion method to convert the output voltage value to PH value.
                        ph = 7 - 1000 * (GrovePhSensor.value-372) * Vref / 59.16 / 1023

                        print("sensor_value =", GrovePhSensor.value, " ph =", ph)

                except IOError:
                        print ("Error")

if __name__ == '__main__':
        main()
