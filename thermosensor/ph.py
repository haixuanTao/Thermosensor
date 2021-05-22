import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
# CLK  = 11
# MISO = 9
# MOSI = 10
# CS   = 8
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
        # The read_adc function will get the value of the specified channel (0-7).
    values = mcp.read_adc(0)
    print(values)
    # Print the ADC values.
    # Pause for half a second.
    time.sleep(0.5)