from prometheus_client import start_http_server, REGISTRY

from adb_prometheus_exporter.collector import AdbTemperatureCollector

REGISTRY.register(AdbTemperatureCollector())


if __name__ == "__main__":
    start_http_server(8000)
    while True:
        pass
