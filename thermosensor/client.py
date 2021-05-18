from prometheus_client.core import (
    GaugeMetricFamily,
    CounterMetricFamily,
    REGISTRY,
)
from prometheus_client import start_http_server
import os
import glob
import time


base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")


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
        yield GaugeMetricFamily("temperature_read", "temperature read", value=0)
        c = CounterMetricFamily(
            "temperature", "Help text", labels=["temperature_sensor"]
        )
        for device in device_folder:
            c.add_metric([device.strip(base_dir)], read_temp(device))
        yield c


REGISTRY.register(CustomCollector())

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        REGISTRY.collect()
        time.sleep(1)
