import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

from ..exceptions import ApktoolError, ApktoolMissingError
from .Zipalign import zipalign


class Apktool:
    exe = "apktool"

    def __init__(self):
        try:
            is_present = subprocess.run(
                [self.exe, "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
            if is_present.returncode != 0:
                raise FileNotFoundError()
        except FileNotFoundError:
            raise ApktoolMissingError(
                f"Apktool not found, please install it from https://github.com/iBotPeaches/Apktool/"
            )

    def unpack(self, input_apk: Path, output_dir: Path):
        result = subprocess.run(
            [self.exe, "d", input_apk, "-f", "-o", output_dir, "-s", "-r"]
        )
        if result.returncode != 0:
            raise ApktoolError("Please refer to the above apktool logs")

    def build(self, input_dir: Path, output_apk: Path):
        with NamedTemporaryFile() as f:
            result = subprocess.run([self.exe, "b", input_dir, "-o", f.name])
            if result.returncode != 0:
                raise ApktoolError("Please refer to the above apktool logs")
            zipalign(f.name, output_apk)

    def libs_path(self):
        return Path("lib")
