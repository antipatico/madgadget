import subprocess
from pathlib import Path

from ..exceptions import ZipalignError


def zipalign(input_apk: str, output_apk: Path):
    result = subprocess.run(["zipalign", "-p", "4", input_apk, output_apk.absolute()])
    if result.returncode != 0:
        raise ZipalignError("Please refer to the above zipalign logs")
