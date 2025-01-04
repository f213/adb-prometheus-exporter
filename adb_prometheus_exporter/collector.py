from adb_prometheus_exporter.adb import Device
from typing import Generator
import contextlib
from prometheus_client.registry import Collector
from prometheus_client.core import GaugeMetricFamily


class AdbTemperatureCollector(Collector):
    def collect(self) -> Generator[GaugeMetricFamily, None, None]:
        devices = Device.list_all(populate=True)
        battery = GaugeMetricFamily("battery_temperature", "Battery temperatur", labels=["device"])
        soc = GaugeMetricFamily("soc_temperature", "SoC temperature", labels=["device"])
        for device in devices:
            with contextlib.suppress(KeyError):
                battery.add_metric([device.serial], float(device.temperatures.bat.value))
            with contextlib.suppress(KeyError):
                soc.add_metric([device.serial], float(device.temperatures.ap.value))

        yield battery
        yield soc


__all__ = ["AdbTemperatureCollector"]
