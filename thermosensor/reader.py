import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import os
import glob

# PH config
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Temperature config
base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")


def read_ph(port=0):
    return mcp.read_adc(port)


def read_temperature(device):
    f = open(device + "/w1_slave", "r")
    lines = f.readlines()
    temp = 0
    if lines[0].strip()[-3:] == "YES":
        equals_position = lines[1].find("t=")
        if equals_position != -1:
            temp_string = lines[1][equals_position + 2 :]
            temp = float(temp_string) / 1000.0
    f.close()
    return temp

