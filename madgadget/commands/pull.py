import sys
from pathlib import Path

from ppadb.client import Client as AdbClient


def pull(package_name: str, output: str | Path | None):
    client = AdbClient(host="127.0.0.1", port=5037)
    device = next(iter(client.devices()))
    if device is None:
        print("ERROR: cannot find any device connected via adb")
        sys.exit(1)
    info = device.shell(f"pm path {package_name}")
    if len(info) == 0:
        print(
            f"ERROR: cannot find package '{package_name}' installed on adb connected device"
        )
        sys.exit(1)
    apks = [p.split(":")[1] for p in info.split()]
    base_apk = apks[0]
    split_config_apks = apks[1:]
    is_split_config = len(split_config_apks) > 0
    if output is None:
        output = package_name + ".madgadget" if is_split_config else Path(base_apk).name
    output = Path(output)
    if is_split_config:
        output.mkdir(exist_ok=True)
        for package in apks:
            device.pull(package, output / Path(package).name)
    else:
        device.pull(base_apk, output)
