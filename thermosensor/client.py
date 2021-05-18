from prometheus_client.core import (
    GaugeMetricFamily,
    CounterMetricFamily,
    REGISTRY,
)
from prometheus_client import start_http_server
import os
import glob
import time


os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")
device_file = device_folder


def read_temp_raw(device_file):
    f = open(device_file, "r")
    lines = f.readlines()
    temp = 0
    if lines[0].strip()[-3:] == "YES":
        equals_position = lines[1].find("t=")
        if equals_position != -1:
            temp_string = lines[1][equals_position + 2 :]
            temp = float(temp_string) / 1000.0
    f.close()
    return temp


def read_temp(device):
    temp = read_temp_raw(device + "/w1_slave")
    return temp


class CustomCollector(object):
    def collect(self):
        yield GaugeMetricFamily("temperature", "temperature read", value=0)
        c = CounterMetricFamily(
            "my_counter_total", "Help text", labels=["total_"]
        )
        for device in device_folder:
            c.add_metric([device], read_temp(device))
        yield c


REGISTRY.register(CustomCollector())

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        read_temp()
        time.sleep(1)
