from prometheus_client import REGISTRY, make_wsgi_app
import os
from wsgiref.simple_server import make_server

from adb_prometheus_exporter.collector import AdbTemperatureCollector, UnauthorizedDeviceCollector

REGISTRY.register(AdbTemperatureCollector())
REGISTRY.register(UnauthorizedDeviceCollector())


if __name__ == "__main__":
    port = os.getenv("PORT", 8000)
    print(f"Starting server on port \033[92m{port}\033[0m...")
    app = make_wsgi_app()
    server = make_server("", 8000, app)
    server.serve_forever()
