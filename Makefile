lint:
	ruff check adb_prometheus_exporter
	mypy adb_prometheus_exporter

fmt:
	ruff format adb_prometheus_exporter

dev:
	watchmedo auto-restart --directory=adb_prometheus_exporter --pattern=*.py --recursive -- python -m adb_prometheus_exporter.exporter
