from collections import UserList
from dataclasses import dataclass, field
from decimal import Decimal
import re
import subprocess


@dataclass
class Temperature:
    sensor: str
    value: Decimal
    type: int
    status: int

    @classmethod
    def from_temperature_line(cls, line) -> "Temperature":
        parsed = dict()
        for line in re.findall(r"(\w+=[^,}]+)", line):
            key, value = line.split("=")
            parsed[key] = value

        return cls(
            sensor=parsed["mName"],
            value=Decimal(parsed["mValue"]),
            type=int(parsed["mType"]),
            status=int(parsed["mStatus"]),
        )


class TemperatureList(UserList[Temperature]):
    def __getattr__(self, name: str) -> Temperature:
        for temperature in self.data:
            if temperature.sensor.lower() == name.lower():
                return temperature
        raise KeyError(f"Temperature sensor {name} not found")


@dataclass
class Device:
    serial: str
    is_authorized: bool = False
    temperatures: TemperatureList = field(default_factory=TemperatureList)

    @classmethod
    def list_all(cls, populate: bool = False) -> list["Device"]:
        result = subprocess.run(["adb", "devices"], capture_output=True)
        if result.returncode != 0:
            raise Exception("Error running `adb devices`")

        devices = []
        for line in result.stdout.decode().split("\n"):
            device_line = line.split("\t")
            if len(device_line) == 2:
                if "unauthorized" not in device_line[1]:
                    device = cls(serial=device_line[0], is_authorized=True)
                    if populate:
                        device.populate()
                    devices.append(device)
                else:
                    devices.append(cls(serial=device_line[0]))

        return devices

    def populate(self) -> None:
        self.fetch_temperature()

    def fetch_temperature(self) -> None:
        result = subprocess.run(
            ["adb", "-s", self.serial, "shell", "dumpsys", "thermalservice"],
            capture_output=True,
        )
        temperatures_are_current = False
        for line in result.stdout.decode().split("\n"):
            if "Current temperatures from HAL" in line:
                temperatures_are_current = True
            if not temperatures_are_current:
                continue
            if "Temperature{" in line:  # } fu, copilot, you ruin my autoindent if i dont close this bracket
                self.temperatures.append(Temperature.from_temperature_line(line))


if __name__ == "__main__":
    temperature_list = TemperatureList(
        [
            Temperature(sensor="cpu", value=Decimal("40.0"), type=1, status=1),
            Temperature(sensor="GpU", value=Decimal("50.0"), type=1, status=1),
        ]
    )

    assert temperature_list.cpu.value == Decimal("40.0"), "__getattr__ should work"
    assert temperature_list.gpu.value == Decimal("50.0"), "__getattr__ should ignore case"
    assert temperature_list.GPU.value == Decimal("50.0"), "__getattr__ should ignore case"

    devices = Device.list_all(populate=True)
    for device in devices:
        print(f"Device \033[94m{device.serial}\033[0m is connected, authorized: \033[92m{device.is_authorized}\033[0m")
        for temperature in device.temperatures:
            print(f"\tSensor \033[92m{temperature.sensor}\033[0m has value \033[92m{temperature.value}\033[0m")
