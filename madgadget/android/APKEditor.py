import subprocess
from pathlib import Path

from ..exceptions import APKEditorError, APKEditorMissingError


class APKEditor:
    exe = "apkeditor"

    def __init__(self):
        try:
            is_present = subprocess.run(
                [self.exe, "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
            if is_present.returncode != 2:
                raise FileNotFoundError()
        except FileNotFoundError:
            raise APKEditorMissingError(
                f"APKEditor not found, please install it from https://github.com/REAndroid/APKEditor/"
            )

    def unpack(self, input_apk: Path, output_dir: Path):
        result = subprocess.run(
            [self.exe, "d", "-i", input_apk, "-f", "-o", output_dir, "-dex"]
        )
        if result.returncode != 0:
            raise APKEditorError("Please refer to the above APKEditor logs")

    def build(self, input_dir: Path, output_apk: Path):
        result = subprocess.run(
            [self.exe, "b", "-i", input_dir, "-f", "-o", output_apk]
        )
        if result.returncode != 0:
            raise APKEditorError("Please refer to the above APKEditor logs")

    def libs_path(self):
        return Path("root") / "lib"
