lint:
	ruff check adb-prometheus-exporter
	mypy adb-prometheus-exporter

fmt:
	ruff format adb-prometheus-exporter
