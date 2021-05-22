from prometheus_client.core import (
    GaugeMetricFamily,
    REGISTRY,
)
from prometheus_client import start_http_server
import time
from reader import read_temperature, base_dir, device_folder, read_ph

class CustomCollector(object):
    def collect(self):
        temperatures = GaugeMetricFamily(
            "temperatures", "Temperature taken from sensors", labels=["temperature_sensor"]
        )
        for device in device_folder:
            temperatures.add_metric([device.strip(base_dir)], read_temperature(device))
        yield temperatures

        phs = GaugeMetricFamily(
            "phs", "PH taken from sensors", labels=["ph_sensor"]
        )
        for i in range(8):
            phs.add_metric([f'ph_channel_{i}'], read_ph(i))
        yield phs


REGISTRY.register(CustomCollector())

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        REGISTRY.collect()
        time.sleep(1)
