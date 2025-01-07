# Prometheus exporter for andorid devices temperature

## Description
Exports android devices temperature metrics to prometheus. Exporter uses [Android debug bridge](https://developer.android.com/tools/adb) (adb) to get the temperature of the device.

## Usage
You need to have adb installed on the host machine. Then authorize the device to use adb. You can do this by running `adb devices` and accepting the prompt on
the device. After that you can run the exporter with the following command:

```bash
$ docker run -v ~/.android:/home/.android -v /dev/bus/usb:/dev/bus/usb --privileged -p 8000:8000  -ti ghcr.io/f213/adb-prometheus-exporter
```
This mounts your adb keys inside of the container. The exporter is available on port 8000, conifgurable with the `PORT` environment variable.

Or the same via docker-compose.yml:
```yaml
---
services:
  exporter:
    image: ghcr.io/f213/adb-prometheus-exporter
    privileged: true
    restart: always
    ports:
      - 8000:8000
    volumes:
      - /root/.android:/home/.android
      - /dev/bus/usb:/dev/bus/usb
```
